"""Extract section structure from each discography page."""
import re
import sys

def extract_sections(page_name: str):
    with open(f"/Users/dmichael/projects/davidmichael.xyz/_reference/site-source/{page_name}.html") as f:
        html = f.read()

    # Split by block containers
    parts = re.split(
        r'<div[^>]*class="block-container[^"]*"[^>]*id="block-container-([^"]+)"[^>]*data-[^>]*data-blockkey="([^"]+)"',
        html
    )

    print(f"=== {page_name} ===\n")
    for i in range(1, len(parts), 3):
        if i + 2 >= len(parts):
            break
        block_key = parts[i + 1]
        content = parts[i + 2][:5000]

        if "footer" in block_key or "header" in block_key:
            continue

        texts = re.findall(r'text__text[^>]*>(.*?)</div>', content, re.DOTALL)
        text_items = []
        for t in texts:
            clean = re.sub(r'<[^>]+>', '', t).strip().replace('&nbsp;', ' ').strip()
            if clean and len(clean) > 3:
                text_items.append(clean)

        imgs = [im.split('/')[-1] for im in re.findall(r'src="([^"]+images-pw[^"]+)"', content)]
        has_bg = 'background-image' in content[:1000] or 'fb-block__background' in content[:1000]
        bg_imgs = [im.split('/')[-1] for im in re.findall(r'fb-block__background-image[^>]+src="([^"]+)"', content)]

        print(f"  [{block_key}]")
        if has_bg:
            print(f"    type: hero/banner")
            for bi in bg_imgs:
                print(f"    bg-img: {bi}")
        for t in text_items:
            print(f"    text: {t[:150]}")
        for im in imgs:
            print(f"    img: {im}")
        print()

pages = sys.argv[1:] if len(sys.argv) > 1 else [
    "the-slaughterhouse",
    "microphones-are-not-ears",
    "mmabolela",
    "el-yunque",
    "shangri-la",
]

for page in pages:
    extract_sections(page)
