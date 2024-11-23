import hashlib
import inspect
import logging
import pickle
import shelve
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def arg_key(args, mark):
    key = mark
    key += args
    return key


def kwarg_key(kwargs, mark):
    key = mark
    for item in kwargs.items():
        key += item
    return key

def func_key(function, mark):
    key = mark
    key += (inspect.getsource(function), )
    return key


def memoize(
    clean: bool = False,
    arg_mark: tuple = (object(),),
    kwarg_mark: tuple = (object(),),
    func_key = func_key,
    arg_key = arg_key,
    kwarg_key = kwarg_key,
    database: str = ".cached",
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key: tuple = func_key(func, mark=(object(),))
            key += arg_key(args, mark=arg_mark)
            key += kwarg_key(kwargs, mark=kwarg_mark)
            hash_key = hashlib.sha256(pickle.dumps(key)).hexdigest()

            with shelve.open(database) as data:
                if hash_key not in data or clean is True:
                    data[hash_key] = func(*args, **kwargs)
                return data[hash_key]

        return wrapper

    return decorator
