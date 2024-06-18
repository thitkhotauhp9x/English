class CacheError(Exception):
    ...


class CacheDecodeError(CacheError):
    ...


class CacheEncodeError(CacheError):
    ...


class CacheKeyError(CacheError):
    ...
