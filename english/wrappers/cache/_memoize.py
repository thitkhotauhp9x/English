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


def memoize(
    clean: bool = False,
    arg_mark: tuple = (object(),),
    kwarg_mark: tuple = (object(),),
    database: str = ".cached",
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key: tuple = (inspect.getsource(func),)
            key += arg_mark
            key += args
            key += kwarg_mark
            for item in kwargs.items():
                key += item
            hash_key = hashlib.sha256(pickle.dumps(key)).hexdigest()

            with shelve.open(database) as data:
                if hash_key not in data or clean is True:
                    data[hash_key] = func(*args, **kwargs)
                return data[hash_key]

        return wrapper

    return decorator
