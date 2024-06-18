import inspect
from dataclasses import dataclass
from typing import Dict, Callable, get_args, Any, Tuple

from english.wrappers import logging
from english.wrappers.cache.annotations import Cache
from english.wrappers.cache.key_makers._base_key_maker import BaseKeyMaker

logger = logging.getLogger(__name__)


def get_kwargs(func, args, kwargs):
    params = inspect.signature(func).parameters
    kwargs.update(dict(zip(params, args)))
    return kwargs


@dataclass
class TypeHintKeyMaker(BaseKeyMaker):
    func: Callable
    args: tuple
    kwargs: Dict[Any, Any]

    def make(self) -> tuple:
        all_kwargs = get_kwargs(self.func, self.args, self.kwargs)

        signature = inspect.signature(self.func)
        params = signature.parameters

        for param_name, param_type in params.items():
            annotation = param_type.annotation

            for arg in get_args(annotation):
                try:
                    value = all_kwargs[param_name]
                    if isinstance(arg, Cache):
                        all_kwargs[param_name] = arg.key(value)
                except KeyError as error:
                    logger.exception(error)
                    continue

        key: Tuple = (inspect.getsource(self.func),)
        key += (object(),)
        for item in all_kwargs.items():
            key += item
        return key


