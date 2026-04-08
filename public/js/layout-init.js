/**
 * Minimal layout initialization for the grid system.
 * Sets CSS variables that the grid system's calc() cascade depends on.
 */

// Add classes that CSS rules depend on
document.documentElement.classList.add('client-side');
document.body.classList.add('client-side');

// Detect scrollbar and set the appropriate class
const hasScrollbar = window.innerWidth > document.documentElement.clientWidth;
const scrollbarClass = hasScrollbar ? 'scrollbar-setting-true' : 'scrollbar-setting-false';
document.documentElement.classList.add(scrollbarClass);
document.body.classList.add(scrollbarClass);

// Scrollbar width detection and --screen-width
function setScrollbarWidth() {
  const w = window.innerWidth - document.documentElement.clientWidth;
  document.documentElement.style.setProperty('--scrollbar-width', `${w}px`);
  document.documentElement.style.setProperty('--screen-width', `calc(100vw - ${w}px)`);
}
setScrollbarWidth();
window.addEventListener('resize', setScrollbarWidth);

// Set --static-vh for mobile browsers where 100vh includes the URL bar
function setStaticVh() {
  document.documentElement.style.setProperty('--static-vh', `${window.innerHeight}px`);
}
setStaticVh();
window.addEventListener('resize', setStaticVh);

// Header height measurement
function setHeaderHeight() {
  const header = document.querySelector('div[role="banner"]');
  const themeContainer = document.querySelector('.theme-container');
  if (!header || !themeContainer) return;
  const wrap = header.querySelector('.fb-block-padding-wrap');
  if (!wrap) return;
  const cs = window.getComputedStyle(wrap);
  const h = parseFloat(cs.height);
  const pt = parseFloat(cs.paddingTop);
  const pb = parseFloat(cs.paddingBottom);
  themeContainer.style.setProperty('--header-height', `${h}px`);
  themeContainer.style.setProperty('--sticky-header-height', `${h - pt - pb}px`);
}
// Run after a short delay to let CSS load
setTimeout(setHeaderHeight, 100);
window.addEventListener('resize', setHeaderHeight);

// Device detection - add class to html element for CSS targeting
function setDevice() {
  const html = document.documentElement;
  html.classList.remove('is-mobile', 'is-tablet', 'is-desktop');
  if (window.matchMedia('(max-width: 767.98px)').matches) {
    html.classList.add('is-mobile');
  } else if (window.matchMedia('(max-width: 991.99px)').matches) {
    html.classList.add('is-tablet');
  } else {
    html.classList.add('is-desktop');
  }
}
setDevice();
window.addEventListener('resize', setDevice);

// Sticky header behavior
(function() {
  const header = document.querySelector('div[role="banner"]');
  const mainBody = document.querySelector('.main-body');
  const wrap = header?.querySelector('.fb-block-padding-wrap');
  if (!header || !mainBody || !wrap) return;

  const isSticky = header.classList.contains('sticky-header');
  const isAbsolute = header.classList.contains('absolute-header');

  if (isSticky) {
    const container = document.querySelector('.page-container');
    if (!container) return;
    setTimeout(() => {
      const headerHeight = header.clientHeight;
      const threshold = isAbsolute ? 20 : headerHeight;
      container.style.overflow = 'visible';
      document.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        if (scrollY > threshold) {
          container.style.overflow = 'visible';
          wrap.classList.add('fb-block-padding-wrap--sticky');
        } else if (scrollY <= 10) {
          wrap.classList.remove('fb-block-padding-wrap--sticky');
        }
      });
    }, 300);
  }
})();

// Nav color transition on scroll
// When a page has a hero/banner image, the nav starts white (over the image)
// and should transition to dark text with an opaque background once scrolled past the hero.
(function() {
  const header = document.querySelector('div[role="banner"]');
  if (!header) return;
  const wrap = header.querySelector('.fb-block-padding-wrap');
  if (!wrap) return;

  // Find the first content block after the header to determine hero height
  const firstBlock = document.querySelector('.main-body .block-container');
  if (!firstBlock) return;

  // Check if the first block has a background image (hero)
  const hasBgImage = firstBlock.querySelector('.fb-block__background-image');
  if (!hasBgImage) return;

  // Get hero height
  const getHeroBottom = () => firstBlock.getBoundingClientRect().bottom + window.scrollY;

  // Add styles for the scrolled state
  const style = document.createElement('style');
  style.textContent = `
    div[role="banner"] .fb-block-padding-wrap.nav-scrolled {
      background-color: var(--primary-background, #F2F2ED) !important;
      transition: background-color 0.3s ease;
    }
    div[role="banner"] .fb-block-padding-wrap.nav-scrolled .navigation__link,
    div[role="banner"] .fb-block-padding-wrap.nav-scrolled .fb-element--logo a,
    div[role="banner"] .fb-block-padding-wrap.nav-scrolled .fb-element--logo span,
    div[role="banner"] .fb-block-padding-wrap.nav-scrolled .site-title,
    div[role="banner"] .fb-block-padding-wrap.nav-scrolled .page-name,
    div[role="banner"] .fb-block-padding-wrap.nav-scrolled .navigation__link--icon {
      color: var(--primary-headings, #23251E) !important;
      transition: color 0.3s ease;
    }
  `;
  document.head.appendChild(style);

  let heroBottom = getHeroBottom();

  const onScroll = () => {
    if (window.scrollY > heroBottom - 80) {
      wrap.classList.add('nav-scrolled');
    } else {
      wrap.classList.remove('nav-scrolled');
    }
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', () => { heroBottom = getHeroBottom(); });
  onScroll();
})();
