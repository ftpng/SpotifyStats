import base64
import aiohttp

from statlib import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN
from statlib.logging import logger


_access_token = None

async def refresh_access_token():
    """
    Request a new Spotify access token using the stored refresh token.

    :return: The new access token string, or None if the request fails.
    """
    global _access_token

    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": REFRESH_TOKEN
            },
            headers={
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        ) as resp:

            data = await resp.json()

            if "access_token" not in data:
                logger.error("Could not refresh Spotify access token.")
                logger.info(data)
                
                return None

            _access_token = data["access_token"]
            return _access_token


async def get_access_token():
    """
    Get the currently cached Spotify access token.
    Refresh the token if not available.

    :return: A valid Spotify access token string.
    """
    global _access_token

    if _access_token is None:
        return await refresh_access_token()

    return _access_token