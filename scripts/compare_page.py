import asyncio
import json
import base64
import sys
import websockets

PAGE_ID = "60E0C30C70D39084CA642046EF189F0D"
OUT = "/Users/dmichael/projects/davidmichael.xyz/_reference"

async def screenshot(url: str, name: str, width: int = 1440, height: int = 900):
    ws_url = f"ws://localhost:9222/devtools/page/{PAGE_ID}"
    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        await ws.send(json.dumps({"id": 0, "method": "Emulation.setDeviceMetricsOverride",
            "params": {"width": width, "height": height, "deviceScaleFactor": 2, "mobile": False}}))
        await ws.recv()
        await ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": url}}))
        await ws.recv()
        await asyncio.sleep(5)
        await ws.send(json.dumps({"id": 2, "method": "Page.captureScreenshot",
            "params": {"format": "jpeg", "quality": 85}}))
        result = json.loads(await ws.recv())
        data = result["result"]["data"]
        path = f"{OUT}/{name}.jpg"
        with open(path, "wb") as f:
            f.write(base64.b64decode(data))
        print(f"Saved {name}.jpg")

async def main():
    page = sys.argv[1] if len(sys.argv) > 1 else "trophies"
    await screenshot(f"https://www.davidmichael.xyz/{page}/", f"original-{page}")
    await screenshot(f"http://localhost:4321/{page}/", f"new-{page}")

asyncio.run(main())
