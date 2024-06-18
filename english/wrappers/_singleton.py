from abc import abstractmethod
from dataclasses import dataclass, field, InitVar


@dataclass
class Product:
    ...


@dataclass
class Builder:
    """

    def build_step_a():
    def build_step_b():
    ...
    """
    product: InitVar[Product]
    _product: Product = field(init=False)

    def __post_init__(self, product: Product) -> None:
        self._product = product

    @abstractmethod
    def reset(self) -> None:
        ...

    @property
    def product(self) -> Product:
        return self._product


@dataclass
class Director:
    """
    director = Director(builder=Builder(product=Product()))
    director.change(Builder(product=Product()))
    """

    builder: InitVar[Builder]
    _builder: Builder = field(init=False)

    def __post_init__(self, builder: Builder) -> None:
        self._builder = builder

    def change(self, builder: Builder) -> None:
        self._builder = builder

    @abstractmethod
    def make(self, category: str) -> None:
        """
        builder.reset()
        if category == "simple"
            self._builder.build_step_a()
        else:
            self._builder.build_step_b()
            self._builder.build_step_c()

        :param category:
        :return:
        """
        raise NotImplementedError()
