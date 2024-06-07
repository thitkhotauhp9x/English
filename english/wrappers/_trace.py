import inspect
from functools import wraps
from pathlib import PosixPath
from typing import Callable, ParamSpec, TypeVar

from english.wrappers._logging import getLogger

logger = getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def trace() -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            params_ = []

            for arg in args:
                arg_type = type(arg).__name__
                if isinstance(arg, PosixPath):
                    size = arg.stat().st_size
                    params_.append(f"{arg_type}(size={size})={arg}")
                else:
                    params_.append(f"{arg_type}={arg}")

            for key, value in kwargs.items():
                value_type = type(value).__name__
                params_.append(f"{key}:{value_type}={value}")

            current_frame = inspect.currentframe()

            scope: str = ""
            if current_frame is not None:
                outer_frames = inspect.getouterframes(current_frame.f_back)
                if len(outer_frames) > 0:
                    func_frame = outer_frames[0]
                    scope = f"{func_frame.filename}::{func_frame.function}::{func_frame.lineno}"

            result = func(*args, **kwargs)

            msg = f"{scope} {func.__name__}({", ".join(params_)}) -> {type(result).__name__}={result}"
            logger.info(msg)
            return result

        return wrapper

    return decorator
