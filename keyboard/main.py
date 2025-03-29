"""Keyboard listener that presses the keys automatically."""

from pyautogui import press
from uvloop import run
from websockets.asyncio.client import connect


async def main():
    """Listen for keypresses."""
    uri = "ws://localhost:1968"
    async with connect(uri) as websocket:
        await websocket.send("keyboard")
        async for message in websocket:
            print(message)
            args = message.split(" ")
            if args[0] == "press":
                key = args[1]
                press(key)


if __name__ == "__main__":
    run(main())
