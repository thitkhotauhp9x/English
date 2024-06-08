from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

from english.wrappers import memoize


def main():
    @memoize
    def func(n1, n2, p, a, b):
        print(p)
        return n1 + n2 + a + b

    with NamedTemporaryFile() as tf:
        path = Path(tf.name)
        path.write_bytes(b"...")
        print(func(1, 2, path, 1, 2))

    with TemporaryDirectory() as td:
        path = Path(td)
        print(func(1, 2, path, 1, 2))


if __name__ == "__main__":
    main()
