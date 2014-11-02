from django.core.cache import cache


def cache_delete_pattern(pattern, version=None, client=None):
    """
    Remove all keys matching pattern.
    """

    pattern = cache.make_key(pattern, version=version)
    keys = cache._client.keys(pattern)

    if keys:
        return cache._client.delete(*keys)
