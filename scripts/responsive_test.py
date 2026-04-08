import asyncio
import json
import base64
import websockets

PAGE_ID = "8ECF871D887BF850F94E20AB58AA1DD0"
OUT = "/Users/dmichael/projects/davidmichael.xyz/_reference"

VIEWPORTS = [
    ("desktop", 1440, 900),
    ("tablet", 768, 1024),
    ("mobile", 375, 812),
]

PAGES = [
    ("/", "home"),
    ("/trophies/", "trophies"),
    ("/the-microphones-gaze/", "mg"),
]

async def screenshot(url: str, name: str, width: int, height: int):
    ws_url = f"ws://localhost:9222/devtools/page/{PAGE_ID}"
    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        await ws.send(json.dumps({"id": 0, "method": "Emulation.setDeviceMetricsOverride",
            "params": {"width": width, "height": height, "deviceScaleFactor": 2, "mobile": width < 768}}))
        await ws.recv()
        await ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": url}}))
        await ws.recv()
        await asyncio.sleep(5)
        await ws.send(json.dumps({"id": 2, "method": "Page.captureScreenshot",
            "params": {"format": "jpeg", "quality": 85}}))
        result = json.loads(await ws.recv())
        with open(f"{OUT}/{name}.jpg", "wb") as f:
            f.write(base64.b64decode(result["result"]["data"]))

async def main():
    for vp_name, w, h in VIEWPORTS:
        for path, page_name in PAGES:
            orig_name = f"resp-orig-{page_name}-{vp_name}"
            new_name = f"resp-new-{page_name}-{vp_name}"
            await screenshot(f"https://www.davidmichael.xyz{path}", orig_name, w, h)
            await screenshot(f"http://localhost:4321{path}", new_name, w, h)
            print(f"  {page_name} @ {vp_name}: done")

asyncio.run(main())
