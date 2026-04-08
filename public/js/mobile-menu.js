/**
 * Mobile menu handler.
 *
 * On mobile (<=767px):
 * - Shows the hamburger button (expand-menu)
 * - Hides the inline nav items
 * - Toggles a fullscreen popup menu on click
 *
 * On desktop (>=992px):
 * - Hides hamburger, shows inline nav
 * - Handles dropdown hover/click for submenus
 */

(function() {
  const menuEl = document.querySelector('.fb-element-type-menu');
  if (!menuEl) return;

  // Add popup class that CSS needs for hamburger line rendering
  function updateMenuType() {
    if (window.matchMedia('(max-width: 991px)').matches) {
      menuEl.classList.add('fb-element-type-menu--popup');
      menuEl.dataset.menuType = 'popup';
    } else {
      menuEl.classList.remove('fb-element-type-menu--popup');
      menuEl.dataset.menuType = 'list';
    }
  }
  updateMenuType();
  window.addEventListener('resize', updateMenuType);

  const expandBtn = menuEl.querySelector('.fb-element-type-menu__expand-menu');
  const navWrapper = menuEl.querySelector('.navigation__wrapper');
  if (!expandBtn || !navWrapper) return;

  // Create a popup overlay for mobile
  const popup = document.createElement('div');
  popup.className = 'mobile-menu-popup';
  popup.innerHTML = navWrapper.innerHTML;
  document.body.appendChild(popup);

  // Style the popup
  const style = document.createElement('style');
  style.textContent = `
    .mobile-menu-popup {
      display: none;
      position: fixed;
      inset: 0;
      background: var(--primary-background, #F2F2ED);
      z-index: 9999;
      overflow-y: auto;
      padding: 5rem 2rem 2rem;
    }
    .mobile-menu-popup.open {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .mobile-menu-popup .navigation__items {
      list-style: none;
      padding: 0;
      margin: 0;
      text-align: center;
    }
    .mobile-menu-popup .navigation__item {
      margin-bottom: 1rem;
    }
    .mobile-menu-popup .navigation__link {
      font-family: var(--font-family, 'Izmir', sans-serif);
      font-size: 1.5rem;
      line-height: 2;
      color: var(--primary-headings, #23251E);
      text-decoration: none;
      letter-spacing: 0.05em;
    }
    .mobile-menu-popup .navigation__link:hover {
      opacity: 0.6;
    }
    .mobile-menu-popup .navigation__item--dropdown {
      display: none;
    }
    .mobile-menu-popup .navigation__item--with-dropdown .navigation__link--folder {
      cursor: pointer;
    }
    .mobile-menu-popup .navigation__item--with-dropdown .js-submenu-dropdown {
      position: static !important;
      transform: none !important;
      opacity: 1 !important;
      display: none;
      margin-top: 0.5rem;
    }
    .mobile-menu-popup .navigation__item--with-dropdown.submenu-open .js-submenu-dropdown {
      display: block;
    }
    .mobile-menu-popup .dropdown-navigation__items {
      list-style: none;
      padding: 0;
    }
    .mobile-menu-popup .dropdown-navigation__link {
      font-size: 1.2rem;
      color: var(--primary-headings, #23251E);
      text-decoration: none;
      line-height: 2;
    }
    .mobile-menu-popup .navigation__link--icon {
      display: inline-block;
      margin-left: 0.5rem;
      font-size: 0.8rem;
    }
    .mobile-menu-close {
      position: absolute;
      top: 1.5rem;
      right: 1.5rem;
      background: none;
      border: none;
      font-size: 1.5rem;
      cursor: pointer;
      color: var(--primary-headings, #23251E);
      padding: 0.5rem;
      line-height: 1;
    }

    /* Show hamburger on mobile + tablet, hide nav items */
    @media (max-width: 991px) {
      .fb-element-type-menu__expand-menu {
        display: block !important;
        width: 30px;
        height: 24px;
        z-index: 10000;
        cursor: pointer;
        align-self: center;
      }
      .navigation__wrapper {
        display: none !important;
      }
    }
    @media (min-width: 992px) {
      .mobile-menu-popup {
        display: none !important;
      }
    }
  `;
  document.head.appendChild(style);

  // Add close button to popup
  const closeBtn = document.createElement('button');
  closeBtn.className = 'mobile-menu-close';
  closeBtn.innerHTML = '✕';
  closeBtn.setAttribute('aria-label', 'Close menu');
  popup.insertBefore(closeBtn, popup.firstChild);

  // Toggle popup
  let isOpen = false;
  function toggleMenu() {
    isOpen = !isOpen;
    popup.classList.toggle('open', isOpen);
    document.documentElement.classList.toggle('ps-no-scroll', isOpen);
    expandBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  }

  expandBtn.addEventListener('click', toggleMenu);
  closeBtn.addEventListener('click', toggleMenu);

  // Handle submenu toggles in popup
  popup.querySelectorAll('.navigation__item--with-dropdown').forEach(item => {
    const trigger = item.querySelector('.js-submenu-trigger, .navigation__link--folder');
    if (trigger) {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        item.classList.toggle('submenu-open');
      });
    }
  });

  // Close menu on link click
  popup.querySelectorAll('a[href]').forEach(link => {
    link.addEventListener('click', () => {
      if (isOpen) toggleMenu();
    });
  });

  // Handle desktop submenu dropdowns (hover)
  if (window.matchMedia('(min-width: 768px)').matches) {
    document.querySelectorAll('.navigation__item--with-dropdown').forEach(item => {
      const dropdown = item.querySelector('.js-submenu-dropdown');
      if (!dropdown) return;

      item.addEventListener('mouseenter', () => {
        dropdown.style.opacity = '1';
        dropdown.style.position = 'absolute';
        dropdown.style.display = 'block';
      });
      item.addEventListener('mouseleave', () => {
        dropdown.style.opacity = '0';
        dropdown.style.display = 'none';
      });
    });
  }
})();
