from math import floor
from random import sample
from string import ascii_lowercase

from uvloop import run
from websockets.asyncio.server import ServerConnection, broadcast, serve
from websockets.exceptions import ConnectionClosedOK

typists = set()
keyboards = set()
typist_letters: dict[ServerConnection, list[str]] = {}


async def reshuffle():
    """Redistribute the letters to typists."""
    letter_list = sample(ascii_lowercase, len(ascii_lowercase))
    starting_indices = []
    for i in range(len(typist_letters)):
        starting_indices.append(floor(i * len(ascii_lowercase) / len(typist_letters)))
    starting_indices.append(len(ascii_lowercase))
    for i, websocket in enumerate(typists):
        typist_letters[websocket] = [letter_list[starting_indices[i]]]
        for j in range(starting_indices[i] + 1, starting_indices[i + 1]):
            typist_letters[websocket].append(letter_list[j])
        await websocket.send(f"assigned {' '.join(typist_letters[websocket])}")


async def handler(websocket):
    """Handle the initial connection and hand off to the correct function."""
    print("client connected")
    try:
        message = await websocket.recv()
    except ConnectionClosedOK:
        print("disconnected")
        return
    args = message.split(" ")
    command = args[0]
    match command:
        case "keyboard":
            await keyboard(websocket)
        case "typist":
            await typist(websocket)


async def keyboard(websocket):
    """Be a keyboard."""
    print("keyboard connected")
    keyboards.add(websocket)
    try:
        async for message in websocket:
            ...
    finally:
        print("keyboard dipped")
        keyboards.remove(websocket)


async def typist(websocket):
    """Be a typist."""
    print("typist connected")
    typists.add(websocket)
    typist_letters[websocket] = {"amogus"}
    await reshuffle()
    try:
        async for message in websocket:
            if message.startswith("press"):
                # Validate key
                split = message.split(" ")
                if len(split) != 2:
                    continue
                key = split[1].strip()
                if not key or key not in ascii_lowercase:
                    continue
                if key not in typist_letters[websocket]:
                    print("not your key")
                    continue
                print(key)
                # Send to keyboard
                broadcast(keyboards, f"press {key}")
    finally:
        # Send typists new keys
        print("typist dipped")
        typists.remove(websocket)
        del typist_letters[websocket]
        await reshuffle()


async def main():
    """Start the server."""
    print("starting server")
    async with serve(handler, "", 1968) as server:
        await server.serve_forever()


if __name__ == "__main__":
    run(main())
