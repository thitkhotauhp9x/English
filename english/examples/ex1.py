from icecream import ic

from english.wrappers import logging

#
# def get_logger(name):
#     logging.basicConfig(
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#         datefmt='%Y-%m-%d %H:%M:%S',
#         level=logging.DEBUG
#     )
#
#     logger = logging.getLogger(name)
#
#     def debug(s):
#         logger.debug(s)
#
#     ic.configureOutput(outputFunction=debug, includeContext=True, contextAbsPath=True)
#     return logger

logger = logging.getLogger(__name__)


logger.debug("abc")
ic('eep')
