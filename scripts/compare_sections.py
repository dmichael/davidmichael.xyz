import asyncio
import json
import base64
import websockets

PAGE_ID = "60E0C30C70D39084CA642046EF189F0D"
OUT = "/Users/dmichael/projects/davidmichael.xyz/_reference"

async def screenshot_at(url: str, name: str, scroll_y: int):
    ws_url = f"ws://localhost:9222/devtools/page/{PAGE_ID}"
    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        await ws.send(json.dumps({"id": 0, "method": "Emulation.setDeviceMetricsOverride",
            "params": {"width": 1440, "height": 900, "deviceScaleFactor": 2, "mobile": False}}))
        await ws.recv()
        await ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": url}}))
        await ws.recv()
        await asyncio.sleep(5)
        await ws.send(json.dumps({"id": 2, "method": "Runtime.evaluate",
            "params": {"expression": f"window.scrollTo(0, {scroll_y})"}}))
        await ws.recv()
        await asyncio.sleep(1)
        await ws.send(json.dumps({"id": 3, "method": "Page.captureScreenshot",
            "params": {"format": "jpeg", "quality": 85}}))
        result = json.loads(await ws.recv())
        with open(f"{OUT}/{name}.jpg", "wb") as f:
            f.write(base64.b64decode(result["result"]["data"]))
        print(f"Saved {name}.jpg")

async def main():
    page = "the-microphones-gaze"
    scrolls = [0, 500, 1000, 1500, 2000, 2500]
    for i, scroll in enumerate(scrolls):
        await screenshot_at(f"https://www.davidmichael.xyz/{page}/", f"orig-mg-{i}", scroll)
        await screenshot_at(f"http://localhost:4321/{page}/", f"new-mg-{i}", scroll)

asyncio.run(main())
