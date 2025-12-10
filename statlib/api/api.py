import aiohttp
from typing import Optional, Dict, Any

from .auth import get_access_token, refresh_access_token
from .cache import get_cache, set_cache


async def spotify_request(endpoint: str, cache_ttl: int = 5) -> Optional[Dict[str, Any]]:
    """
    Send a request to the Spotify Web API with caching and auto-refresh token logic.

    :param endpoint: The Spotify API endpoint, e.g., '/v1/me/player/currently-playing'.
    :param cache_ttl: Number of seconds to cache the response.
    :return: Parsed JSON response or None.
    """
    cached = get_cache(endpoint)
    if cached:
        return cached

    token = await get_access_token()
    url = f"https://api.spotify.com{endpoint}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"Authorization": f"Bearer {token}"}) as resp:
            if resp.status == 401:
                await refresh_access_token()
                return await spotify_request(endpoint, cache_ttl)

            if resp.status == 204:
                return None

            data = await resp.json()
            set_cache(endpoint, data, cache_ttl)
            return data


async def get_now_playing() -> Optional[Dict[str, Any]]:
    """
    Retrieve detailed data about the currently playing Spotify track.

    :return: A dictionary containing track details, playback state, and progress, or None.
    """
    data = await spotify_request("/v1/me/player/currently-playing", cache_ttl=1)

    if not data or "item" not in data:
        return None

    item = data["item"]

    return {
        "track": item["name"],
        "artist": item["artists"][0]["name"],
        "url": item["external_urls"]["spotify"],
        "thumbnail": item["album"]["images"][0]["url"],
        "progress_ms": data.get("progress_ms", 0),
        "is_playing": data.get("is_playing", False)
    }