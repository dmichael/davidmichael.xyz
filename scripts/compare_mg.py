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
    # Just top and first scroll for quick iteration
    for scroll in [0, 600]:
        label = "top" if scroll == 0 else "mid"
        await screenshot_at("https://www.davidmichael.xyz/the-microphones-gaze/", f"orig-mg-{label}", scroll)
        await screenshot_at("http://localhost:4321/the-microphones-gaze/", f"new-mg-{label}", scroll)

asyncio.run(main())
