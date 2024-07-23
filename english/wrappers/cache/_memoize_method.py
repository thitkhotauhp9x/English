# import logging
# import pickle
# from functools import wraps
# from typing import Callable, ParamSpec, TypeVar, get_args, Tuple, get_type_hints, Any, Dict
#
# from english.wrappers.cache.annotations import Cache
# from english.wrappers.cache.errors import CacheError, CacheKeyError
# from english.wrappers.cache.key_makers import TypeHintKeyMaker, KeyMaker, DictKeyMaker
#
# logger = logging.getLogger(__name__)
#
# P = ParamSpec("P")
# R = TypeVar("R")
#
#
# def make_attributes_key(self: Any, attributes: Tuple[str]) -> Tuple:
#     key: tuple = (object(),)
#     for attribute in attributes:
#         type_hints = get_type_hints(self, include_extras=True)
#         type_hint = type_hints[attribute]
#         value = getattr(self, attribute)
#
#         for arg in get_args(type_hint):
#             if isinstance(arg, Cache):
#                 value = arg.key(value)
#         key += (attribute, value)
#     return key
#
#
# def memoize_method(
#     encode: Callable[[R], bytes] = pickle.dumps,
#     decode: Callable[[bytes], R] = pickle.loads,
#     attributes: Tuple[Any] = (None,),
# ) -> Callable[[Callable[P, R]], Callable[P, R]]:
#     def decorator(func: Callable[P, R]) -> Callable[P, R]:
#         cache = {}
#
#         @wraps(func)
#         def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:
#             try:
#                 attrs = {}
#                 for attr in attributes:
#                     type_hint = get_type_hints(self, include_extras=True)[attr]
#
#                     value = getattr(self, attr)
#                     for arg in get_args(type_hint):
#                         try:
#                             if isinstance(arg, Cache):
#                                 value = arg.key(value)
#                         except KeyError as error:
#                             logger.exception(error)
#                             continue
#                     attrs[attr] = value
#
#                 key = make_key(func, args, kwargs, attrs)
#
#                 if key not in cache:
#                     result = func(*args, **kwargs)
#                     cache[key] = encode(result)
#                 return decode(cache[key])
#             except CacheError as error:
#                 logger.exception(error)
#                 return func(self, *args, **kwargs)
#
#         return wrapper
#
#     return decorator
#
#
# def make_key(func, args, kwargs: Dict[Any, Any], attrs):
#     try:
#         maker = KeyMaker()
#         maker.add_maker(TypeHintKeyMaker(func, args, kwargs).hash())
#         maker.add_maker(DictKeyMaker(attrs))
#         return maker.hash()
#     except Exception as error:
#         raise CacheKeyError() from error
