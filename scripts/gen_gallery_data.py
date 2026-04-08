"""Generate gallery image data from crawled HTML for use in Astro pages."""
import re
import json
import sys

def extract_gallery(page_name: str):
    with open(f"/Users/dmichael/projects/davidmichael.xyz/_reference/site-source/{page_name}.html") as f:
        html = f.read()

    # Hero image
    hero_srcs = re.findall(r'fb-block__background-image[^>]+src="([^"]+)"', html)
    hero_srcsets = re.findall(r'fb-block__background-image[^>]+srcset="([^"]+)"', html)

    hero = None
    if hero_srcs:
        hero_fname = hero_srcs[0].split("/")[-1]
        sizes = {}
        if hero_srcsets:
            for part in hero_srcsets[0].split(","):
                part = part.strip()
                url, w = part.rsplit(" ", 1)
                fname = url.strip().split("/")[-1]
                sizes[w] = fname
        hero = {"default": hero_fname, "sizes": sizes}

    # Gallery images in order
    gallery_imgs = re.findall(
        r'photoswipe-lightbox--image[^>]+src="([^"]+)"[^>]*srcset="([^"]+)"',
        html
    )

    gallery = []
    for src, srcset in gallery_imgs:
        default_fname = src.split("/")[-1]
        sizes = {}
        for part in srcset.split(","):
            part = part.strip()
            url, w = part.rsplit(" ", 1)
            fname = url.strip().split("/")[-1]
            sizes[w] = fname
        gallery.append({"default": default_fname, "sizes": sizes})

    # Title
    titles = re.findall(r'<h[12][^>]*>(.*?)</h[12]>', html, re.DOTALL)
    title = ""
    for t in titles:
        clean = re.sub(r'<[^>]+>', '', t).strip()
        if clean:
            title = clean
            break

    return {"title": title, "hero": hero, "gallery": gallery}

page = sys.argv[1] if len(sys.argv) > 1 else "trophies"
data = extract_gallery(page)
print(json.dumps(data, indent=2))
