# Project: davidmichael.xyz

Static site clone of davidmichael.xyz, built with Astro and served from GitHub Pages.

## Architecture

- **Astro** static site generator, **bun** package manager
- Pages are converted from the original HTML source (`_reference/site-source/`)
- Original vendor CSS is served directly (`public/css/base.css`)
- Images at all responsive sizes in `public/images/`
- Fonts (Izmir) in `public/fonts/`
- Minimal JS for layout init and mobile menu (`public/js/`)

## Key Rule: Reference the Original Implementation

When something doesn't visually match the original site, **do not guess at CSS values or iteratively tweak numbers.** Instead:

1. Inspect how the original achieves it — read the CSS selectors in `base.css`
2. Check what classes, data attributes, or CSS variables are present on the original's DOM (use CDP to query the live site)
3. Replicate those conditions (add the missing class, set the variable, match the selector)

The answer is almost always a missing class gate, a CSS variable that needs to be set, or a selector condition that isn't met. The original CSS already handles the layout correctly — the job is to ensure the right conditions are present for it to activate.

**Do not** write new CSS to approximate what the existing vendor CSS already does.

## Conversion Pipeline

`scripts/convert_pages.py` converts crawled HTML into Astro pages:
- Strips JS, tracking, analytics
- Rewrites image/font URLs to local paths
- Adds `client-side` and `scrollbar-setting-false` classes (required by CSS breakpoints)
- Injects `layout-init.js` and `mobile-menu.js`

## Layout Dependencies

The CSS grid requires:
- `.client-side` class on `<html>` — gates mobile grid column switch (24 → 8 columns)
- `.scrollbar-setting-false` class on `<html>` — gates grid calculations
- `--screen-width` CSS variable — set by `layout-init.js`
- `fb-element-type-menu--popup` class on menu element at mobile — gates hamburger line rendering

## Dev Server

```
bun run dev  # http://localhost:4321/
```

## Comparing with Original

Use CDP (Chrome DevTools Protocol) to browse the live site at davidmichael.xyz via a real Chrome instance (Cloudflare blocks headless browsers). Scripts in `scripts/` handle screenshots and comparison.
