# pylint: disable=invalid-name

import logging
from functools import lru_cache
from logging import Logger

from icecream import ic

__all__ = ["getLogger"]


@lru_cache(maxsize=None)
def init_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.DEBUG,
    )

def getLogger(name: str) -> Logger:
    init_logging()
    logger = logging.getLogger(name)

    def debug(msg: str) -> None:
        logger.debug(msg)

    ic.configureOutput(includeContext=True, contextAbsPath=True, outputFunction=debug)
    return logger
