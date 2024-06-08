import inspect
import logging
from functools import wraps
from pathlib import PosixPath
from typing import Callable, ParamSpec, TypeVar, Any, Dict

__all__ = ["memoize"]

P = ParamSpec("P")
R = TypeVar("R")


def make_key(args, kwargs):
    key = args

    if kwargs:
        key += (object(),)
        for item in kwargs.items():
            key += item

    return hash(key)


def get_kwargs(func, args, kwargs):
    params = inspect.signature(func).parameters
    kwargs_ = dict(zip(params, args))
    kwargs_.update(kwargs)
    return kwargs_


def memoize(func: Callable[P, R]) -> Callable[P, R]:
    cache = {}

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        kwargs_: Dict[Any, Any] = {}
        for key, value in get_kwargs(func, args, kwargs).items():
            if isinstance(value, PosixPath):
                if value.is_file():
                    content = value.read_bytes()
                    kwargs_[key] = content
                elif value.is_dir():
                    logging.warning("Does not support to cache a dir.")
                    kwargs_[key] = value
                else:
                    raise NotImplementedError()
            else:
                kwargs_[key] = value

        key = make_key((), kwargs_)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper
