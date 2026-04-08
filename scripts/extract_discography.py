"""Extract structured content from discography pages."""
import re
import json
import sys

def extract_page(page_name: str):
    with open(f"/Users/dmichael/projects/davidmichael.xyz/_reference/site-source/{page_name}.html") as f:
        html = f.read()

    # Title
    titles = re.findall(r'<h[12][^>]*>(.*?)</h[12]>', html, re.DOTALL)
    title = ""
    for t in titles:
        clean = re.sub(r'<[^>]+>', '', t).strip()
        if clean and clean != "David Michael":
            title = clean
            break

    # Hero image
    hero_srcs = re.findall(r'fb-block__background-image[^>]+src="([^"]+)"', html)
    hero = None
    if hero_srcs:
        hero = hero_srcs[0].split("/")[-1]

    # Object position for hero
    ops = re.findall(r'object-position\s*:\s*([^;"<>]+)', html)
    hero_focus = ops[0].strip() if ops else "50% 50%"

    # All text blocks
    texts = re.findall(r'class="[^"]*text__text[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
    text_blocks = []
    for t in texts:
        clean = re.sub(r'<[^>]+>', '', t).strip()
        clean = clean.replace('&nbsp;', ' ').strip()
        if len(clean) > 10 and clean != title and "© 2026" not in clean and "David Michael" != clean:
            text_blocks.append(clean)

    # All images (not hero, not nav)
    imgs = re.findall(r'<img[^>]+src="([^"]+images-pw[^"]+)"', html)
    images = []
    for img in imgs:
        fname = img.split("/")[-1]
        if hero and fname == hero:
            continue
        images.append(fname)

    # Subtitle (usually the second text block, shorter)
    subtitle = ""
    if len(text_blocks) > 0 and len(text_blocks[0]) < 100:
        subtitle = text_blocks[0]
        text_blocks = text_blocks[1:]

    # Credits (usually short, contains "Recorded" or "edited" or a year)
    credits = ""
    for i, block in enumerate(text_blocks):
        if any(kw in block.lower() for kw in ["recorded", "edited", "mixed", "mastered", "gruenrekorder", "and/oar", "label"]):
            if len(block) < 300:
                credits = block
                text_blocks = text_blocks[:i] + text_blocks[i+1:]
                break

    return {
        "title": title,
        "subtitle": subtitle,
        "credits": credits,
        "hero": hero,
        "heroFocus": hero_focus,
        "images": images,
        "textBlocks": text_blocks,
    }

pages = [
    "the-microphones-gaze",
    "the-slaughterhouse",
    "microphones-are-not-ears",
    "mmabolela",
    "el-yunque",
    "shangri-la",
]

if len(sys.argv) > 1:
    pages = [sys.argv[1]]

for page in pages:
    data = extract_page(page)
    outpath = f"/Users/dmichael/projects/davidmichael.xyz/src/data/{page}.json"
    with open(outpath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"{page}: title='{data['title']}', subtitle='{data['subtitle'][:50]}', hero={'yes' if data['hero'] else 'no'}, images={len(data['images'])}, text={len(data['textBlocks'])} blocks")
