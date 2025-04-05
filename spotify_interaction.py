import spotify
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CLIENT_ID: str = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET: str = os.getenv("SPOTIFY_CLIENT_SECRET")
ALBUM_URI: str = os.getenv("SPOTIFY_ALBUM_URI")

async def get_album_tracks(ident: str, secret: str, album_uri: str) -> None:
    # Useful tip: use a context manager to handle
    # automatically closing any underlying http sessions
    async with spotify.Client(ident, secret) as client:
        album = await client.get_album(album_uri)

        async for track in album:
            print(repr(track))

asyncio.run(get_album_tracks(CLIENT_ID, CLIENT_SECRET, ALBUM_URI))