import time

_cache = {}


def set_cache(key: str, value, ttl: int = 10):
    """
    Store a value in cache with a specified TTL.

    :param key: The cache key identifier.
    :param value: The data to store under the key.
    :param ttl: Time-to-live in seconds before the cache expires.
    """
    _cache[key] = (value, time.time() + ttl)


def get_cache(key: str):
    """
    Retrieve a cached value if it is still valid.

    :param key: The cache key identifier.
    :return: The cached value or None if expired or missing.
    """
    if key not in _cache:
        return None

    value, expires_at = _cache[key]
    if time.time() > expires_at:
        del _cache[key]
        return None

    return value