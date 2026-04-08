"""Extract the complete grid layout for a page."""
import re
import json
import sys

def extract_grid(page_name: str):
    with open(f"/Users/dmichael/projects/davidmichael.xyz/_reference/site-source/{page_name}.html") as f:
        html = f.read()

    # Split by block containers
    parts = re.split(
        r'<div[^>]*class="block-container[^"]*"[^>]*id="block-container-([^"]+)"[^>]*data-[^>]*data-blockkey="([^"]+)"',
        html
    )

    blocks = []
    for i in range(1, len(parts), 3):
        if i + 2 >= len(parts):
            break
        block_id = parts[i]
        block_key = parts[i + 1]
        content = parts[i + 2]

        if "footer" in block_key or "header-style" in block_key:
            continue

        # Block-level CSS from the inline styles
        block_css = {}
        block_rules = re.findall(rf'#{re.escape("block-container-" + block_id)}[^{{}}]*\{{([^}}]+)\}}', html)
        for rule in block_rules:
            pairs = re.findall(r'(--[\w-]+)\s*:\s*([^;]+)', rule)
            for k, v in pairs:
                block_css[k] = v.strip()

        # Find elements in this block
        elements = []
        el_matches = re.finditer(
            r'class="fb-element[^"]*fb-element--el-([a-z0-9]+)[^"]*"[^>]*>',
            content
        )
        for em in el_matches:
            el_id = em.group(1)
            # Get element content (text, images)
            el_start = em.end()
            # Find the element's content div
            el_content = content[el_start:el_start + 2000]

            # Extract text
            texts = re.findall(r'text__text[^>]*>(.*?)</div>', el_content, re.DOTALL)
            text = ""
            for t in texts:
                clean = re.sub(r'<[^>]+>', '', t).strip().replace('&nbsp;', ' ').strip()
                if clean:
                    text = clean

            # Extract image
            imgs = re.findall(r'src="([^"]+images-pw[^"]+)"', el_content)
            img = imgs[0].split("/")[-1] if imgs else None

            # Background image
            bg_imgs = re.findall(r'fb-block__background-image[^>]+src="([^"]+)"', el_content)
            bg_img = bg_imgs[0].split("/")[-1] if bg_imgs else None

            # Element CSS - get all breakpoint variants
            el_rules = re.findall(rf'\.fb-element--el-{el_id}\{{([^}}]+)\}}', html)
            el_css = []
            for rule in el_rules:
                pairs = dict(re.findall(r'(--[\w-]+)\s*:\s*([^;]+)', rule))
                if pairs:
                    el_css.append(pairs)

            # Determine element type
            el_type = "text"
            if bg_img:
                el_type = "bg-image"
            elif img:
                el_type = "image"
            elif 'fb-element--socialLinks' in content[em.start()-200:em.start()+50]:
                el_type = "social"
            elif 'fb-element--backToTop' in content[em.start()-200:em.start()+50]:
                el_type = "back-to-top"

            elements.append({
                "id": el_id,
                "type": el_type,
                "text": text[:300] if text else None,
                "image": img,
                "bgImage": bg_img,
                "css": el_css,  # [desktop, tablet, mobile] typically
            })

        blocks.append({
            "id": block_id,
            "key": block_key,
            "css": block_css,
            "elements": elements,
        })

    return blocks

page = sys.argv[1] if len(sys.argv) > 1 else "the-microphones-gaze"
blocks = extract_grid(page)
print(json.dumps(blocks, indent=2))
