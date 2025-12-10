from typing import Optional
from statlib.api import spotify_request


async def get_artist_image(artist_name: str) -> Optional[str]:
    """
    Retrieve the Spotify profile image URL for the given artist.

    :param artist_name: Name of the artist to search for.
    :return: The highest-resolution artist image URL, or None if unavailable.
    """
    query = artist_name.replace(" ", "%20")
    data = await spotify_request(f"/v1/search?q={query}&type=artist&limit=1")

    items = data.get("artists", {}).get("items", [])
    if items and items[0].get("images"):
        return items[0]["images"][0]["url"]

    return None



async def get_track_image(track_name: str, artist_name: str) -> Optional[str]:
    """
    Retrieve the album artwork URL associated with a track.

    :param track_name: Name of the track to search for.
    :param artist_name: Optional artist name used to refine the search.
    :return: The highest-resolution album image URL, or None if unavailable.
    """
    query = f"{track_name} artist:{artist_name}".replace(" ", "%20")
    data = await spotify_request(f"/v1/search?q={query}&type=track&limit=1")

    items = data.get("tracks", {}).get("items", [])
    if items and items[0]["album"]["images"]:
        return items[0]["album"]["images"][0]["url"]

    return None


async def get_artist_genres(artist_name: str) -> list[str]:
    """
    Fetch the genres for a given artist from Spotify.

    :param artist_name: Name of the artist.
    :return: A list of genres or an empty list.
    """
    query = artist_name.replace(" ", "%20")
    data = await spotify_request(f"/v1/search?q={query}&type=artist&limit=1")

    items = data.get("artists", {}).get("items", [])
    if not items:
        return []

    return items[0].get("genres", []) or []