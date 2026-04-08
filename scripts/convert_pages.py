"""
Convert crawled HTML pages into clean Astro pages.

Strategy:
- Keep all the CSS (inline styles, style blocks)
- Keep the HTML structure and class names
- Strip: vendor JS, tracking, Sentry, analytics, footer badge
- Rewrite image URLs to local paths
- Rewrite font URLs to local paths
- All asset paths are relative (no leading /) for <base href> compatibility
- Wrap in a minimal HTML shell (Astro provides the doctype/head)
"""
import re
import os

SITE_DIR = "/Users/dmichael/projects/davidmichael.xyz/_reference/site-source"
OUT_DIR = "/Users/dmichael/projects/davidmichael.xyz/src/pages"

PAGES = {
    "homepage": "index",
    "trophies": "trophies",
    "landscapes": "landscapes",
    "the-microphones-gaze": "the-microphones-gaze",
    "the-slaughterhouse": "the-slaughterhouse",
    "microphones-are-not-ears": "microphones-are-not-ears",
    "mmabolela": "mmabolela",
    "el-yunque": "el-yunque",
    "shangri-la": "shangri-la",
    "writing": "writing",
}

def clean_page(html: str, page_name: str) -> str:
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', html)
    title = title_match.group(1) if title_match else "David Michael"

    # Extract all <style> blocks
    styles = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
    combined_css = "\n".join(s for s in styles if s.strip())

    # Rewrite font URLs to local (relative, no leading slash)
    combined_css = re.sub(
        r'url\(["\']?https?://fonts-pw\.pixieset\.com/fonts/izmir/([^"\'?\s)]+)[^"\')\s]*["\']?\)',
        r'url("fonts/\1")',
        combined_css
    )
    combined_css = re.sub(
        r'url\(["\']?//fonts-pw\.pixieset\.com/fonts/izmir/([^"\'?\s)]+)[^"\')\s]*["\']?\)',
        r'url("fonts/\1")',
        combined_css
    )

    # Extract body content between <body> and </body>
    body_match = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL)
    if not body_match:
        return ""
    body = body_match.group(1)

    # Remove all <script> tags
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    body = re.sub(r'<noscript[^>]*>.*?</noscript>', '', body, flags=re.DOTALL)

    # Remove footer badge
    body = re.sub(r'<div class="footer-badge">.*?</div>\s*</div>\s*</div>', '', body, flags=re.DOTALL)

    # Remove data attributes we don't need (tracking, etc)
    body = re.sub(r'\s*data-uuid="[^"]*"', '', body)
    body = re.sub(r'\s*data-idhash="[^"]*"', '', body)
    body = re.sub(r'\s*data-blockkey="[^"]*"', '', body)
    body = re.sub(r'\s*data-section="[^"]*"', '', body)

    # Fix accessibility: add href="#" to submenu trigger anchors missing href
    body = re.sub(
        r'<a class="navigation__link navigation__link--folder js-menu-link js-submenu-trigger"',
        '<a href="#" class="navigation__link navigation__link--folder js-menu-link js-submenu-trigger"',
        body
    )

    # Rewrite image URLs to local paths (relative, no leading slash)
    img_page = page_name if page_name != "index" else "homepage"
    body = re.sub(
        r'(src|srcset)="//images-pw\.pixieset\.com/site/[^/]+/[^/]+/([^"]+)"',
        lambda m: f'{m.group(1)}="images/{img_page}/{m.group(2)}"',
        body
    )
    # Handle srcset entries (space-separated URLs within srcset attribute)
    body = re.sub(
        r'//images-pw\.pixieset\.com/site/[^/]+/[^/]+/([^\s,"]+)',
        lambda m: f'images/{img_page}/{m.group(1)}',
        body
    )

    # Also rewrite CSS background images if any (relative)
    combined_css = re.sub(
        r'//images-pw\.pixieset\.com/site/[^/]+/[^/]+/([^\s,"\')\]]+)',
        lambda m: f'images/{img_page}/{m.group(1)}',
        combined_css
    )

    # Remove the external CSS link (we'll inline everything)
    body = re.sub(r'<link[^>]+flex-clientStyles[^>]+>', '', body)
    body = re.sub(r'<link[^>]+flex\.v-[^>]+>', '', body)

    # Remove modulepreload links
    body = re.sub(r'<link[^>]+modulepreload[^>]+>', '', body)
    body = re.sub(r'<link[^>]+preload[^>]+as="style"[^>]+>', '', body)
    body = re.sub(r'<link[^>]+preconnect[^>]+>', '', body)

    # Ensure body has proper open/close tags and add our classes + scripts
    # Add required classes to <body> - include theme-flex which gates 14 CSS rules
    body = re.sub(
        r'<body([^>]*)class="([^"]*)"',
        r'<body\1class="client-side scrollbar-setting-false theme-flex \2"',
        body
    )

    # Rewrite navigation hrefs from absolute to relative (strip leading /)
    # e.g. href="/trophies/" -> href="trophies/"
    # But preserve href="#" and href="https://..." and href="mailto:..."
    body = re.sub(
        r'href="/([^"]*)"',
        r'href="\1"',
        body
    )

    # Inject scripts before </body> or at the end (relative paths)
    scripts = """
<script is:inline src="js/layout-init.js"></script>
<script is:inline src="js/mobile-menu.js" defer></script>
"""
    if '</body>' in body:
        body = body.replace('</body>', scripts + '</body>')
    else:
        body = body + scripts

    # Build the Astro page with <base href> for path resolution
    astro_page = f"""---
// Auto-generated. Title: {title}
// Ensure trailing slash so <base> resolves relative paths correctly
const rawBase = import.meta.env.BASE_URL;
const base = rawBase.endsWith('/') ? rawBase : rawBase + '/';
---
<!doctype html>
<html lang="en" class="client-side scrollbar-setting-false">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <base href={{base}} />
  <title>{title}</title>
  <link rel="stylesheet" href="css/base.css" />
  <link rel="stylesheet" href="css/icons.css" />
  <link rel="stylesheet" href="css/grid-init.css" />
  <style set:html={{`{combined_css}`}} />
</head>
{body}
</html>
"""
    return astro_page


# First, copy the external CSS to public
os.makedirs("/Users/dmichael/projects/davidmichael.xyz/public/css", exist_ok=True)

for src_name, out_name in PAGES.items():
    src_path = os.path.join(SITE_DIR, f"{src_name}.html")
    out_path = os.path.join(OUT_DIR, f"{out_name}.astro")

    with open(src_path) as f:
        html = f.read()

    result = clean_page(html, out_name)

    with open(out_path, "w") as f:
        f.write(result)

    print(f"  {src_name} -> {out_name}.astro ({len(result):,} chars)")

print("\nDone. Now copy the base CSS.")
