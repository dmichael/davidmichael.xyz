import asyncio
import json
import base64
import websockets

PAGE_ID = "60E0C30C70D39084CA642046EF189F0D"
OUT = "/Users/dmichael/projects/davidmichael.xyz/_reference"

async def screenshot(url: str, name: str):
    ws_url = f"ws://localhost:9222/devtools/page/{PAGE_ID}"
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": url}}))
        await ws.recv()
        await asyncio.sleep(4)
        await ws.send(json.dumps({"id": 2, "method": "Page.captureScreenshot",
            "params": {"format": "jpeg", "quality": 80}}))
        result = json.loads(await ws.recv())
        data = result["result"]["data"]
        path = f"{OUT}/{name}.jpg"
        with open(path, "wb") as f:
            f.write(base64.b64decode(data))
        print(f"Saved {name}.jpg")

async def main():
    await screenshot("https://www.davidmichael.xyz/", "original-home")
    await screenshot("http://localhost:4321/", "new-home")

asyncio.run(main())
