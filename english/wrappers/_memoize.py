import hashlib
import inspect
import logging
import pickle
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Callable, ParamSpec, TypeVar, Any, get_args, Tuple

logger = logging.getLogger(__name__)

__all__ = ["memoize", "Cache", "CachePath", "SkipCache"]

P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class Cache(ABC):
    @abstractmethod
    def key(self, value: Any) -> bytes:
        raise NotImplementedError()


@dataclass
class CachePath(Cache):
    def key(self, value: Path) -> bytes:
        return value.read_bytes()


@dataclass
class SkipCache(Cache):
    def key(self, value: Any) -> bytes:
        return pickle.dumps((object(), "skip"))


class CacheError(Exception):
    ...


class CacheDecodeError(CacheError):
    ...


class CacheEncodeError(CacheError):
    ...


class CacheKeyError(CacheError):
    ...


def _get_kwargs(func, args, kwargs):
    params = inspect.signature(func).parameters
    kwargs_ = dict(zip(params, args))
    kwargs_.update(kwargs)
    return kwargs_


def _make_key(func, args, kwargs) -> str:
    key: Tuple = (inspect.getsource(func),)
    key += tuple(args)
    if kwargs:
        key += (object(),)
        for item in kwargs.items():
            key += item

    return hashlib.sha256(pickle.dumps(key)).hexdigest()


def make_key(func, args, kwargs) -> str:
    try:
        kwargs_ = _get_kwargs(func, args, kwargs)

        signature = inspect.signature(func)
        params = signature.parameters

        for param_name, param_type in params.items():
            annotation = param_type.annotation

            for arg in get_args(annotation):
                try:
                    value = kwargs_[param_name]
                    if isinstance(arg, Cache):
                        kwargs_[param_name] = arg.key(value)
                except KeyError as error:
                    logger.exception(error)
                    continue

        key = _make_key(func, (), kwargs_)
        return key
    except Exception as error:
        raise CacheKeyError() from error


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
