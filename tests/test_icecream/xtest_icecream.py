import json
import logging

from icecream import ic, argumentToString

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)


@argumentToString.register(str)
def _(obj):
    return "[!string %r with length %i!]" % (obj, len(obj))


@argumentToString.register(dict)
def _(obj):
    try:
        return json.dumps(obj, indent=2)
    except TypeError:
        return repr(obj)


def debug(msg):
    logging.debug(msg)


ic.configureOutput(includeContext=True, contextAbsPath=True, outputFunction=debug)
a = {
    "1" : "a",
    "b": [
        1, 2, 3
    ]
}

ic(a)
ic("abc")
