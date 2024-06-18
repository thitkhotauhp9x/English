import inspect
from typing import ParamSpec, TypeVar, Callable, NamedTuple, Any, Generator, Annotated

from icecream import ic

P = ParamSpec("P")
T = TypeVar("T")


class Parameter(NamedTuple):
    name: str
    type: str
    value: Any
    metadata: tuple


def get_parameters(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> Generator[Parameter, None, None]:
    parameters = inspect.signature(func).parameters

    all_kwargs = dict(zip(parameters, args))
    all_kwargs.update(kwargs)

    for param_name, param_type in parameters.items():
        metadata = getattr(param_type.annotation, "__metadata__", None)
        param_value = all_kwargs[param_name]

        yield Parameter(name=param_name, value=param_value, metadata=metadata)


def add(a, b: Annotated[int, str]):
    return a + b


for p in get_parameters(add, 1, b=2):
    ic(p)
a = Annotated[int, str]
ic(a.mro())
