# pylint: disable=invalid-name

import logging
from functools import lru_cache
from logging import INFO, Logger

__all__ = ["getLogger"]


@lru_cache(maxsize=None)
def init_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=INFO,
    )


def getLogger(name: str) -> Logger:
    init_logging()
    return logging.getLogger(name)
