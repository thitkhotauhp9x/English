import logging
import pickle
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from english.wrappers.cache.errors import CacheEncodeError, CacheDecodeError, CacheError, CacheKeyError
from english.wrappers.cache.key_makers import TypeHintKeyMaker

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def memoize(
    encode: Callable[[R], bytes] = pickle.dumps,
    decode: Callable[[bytes], R] = pickle.loads,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        cache = {}

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                key = make_key(func, args, kwargs)
                if key not in cache:
                    result = func(*args, **kwargs)
                    try:
                        cache[key] = encode(result)
                    except Exception as error:
                        raise CacheEncodeError() from error
                try:
                    return decode(cache[key])
                except Exception as error:
                    del cache[key]
                    raise CacheDecodeError() from error
            except CacheError as error:
                logger.exception(error)
                return func(*args, **kwargs)

        return wrapper

    return decorator


def make_key(func, args, kwargs) -> str:
    try:
        return TypeHintKeyMaker(func, args, kwargs).hash()
    except Exception as error:
        raise CacheKeyError() from error
