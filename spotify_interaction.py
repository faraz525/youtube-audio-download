import spotify

import asyncio

CLIENT_ID: str = "66f71e1f4f4a4cb0918c9f4a8dd67639"
CLIENT_SECRET: str = "8e632b78c6884e89a69a3543adae2a81"
ALBUM_URI: str = "spotify:album:4aawyAB9vmqN3uQ7FjRGTy"

async def get_album_tracks(ident: str, secret: str, album_uri: str) -> None:
    # Useful tip: use a context manager to handle
    # automatically closing any underlying http sessions
    async with spotify.Client(ident, secret) as client:
        album = await client.get_album(album_uri)

        async for track in album:
            print(repr(track))

asyncio.run(get_album_tracks(CLIENT_ID, CLIENT_SECRET, ALBUM_URI))