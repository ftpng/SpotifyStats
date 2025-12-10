from os import getenv
from typing import Text
from dotenv import load_dotenv; load_dotenv()


TOKEN: Text = getenv('TOKEN')
CLIENT_ID: Text = getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET: Text = getenv("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN : Text= getenv("SPOTIFY_REFRESH_TOKEN")

EMBED_COLOR: str = 0x393a41 