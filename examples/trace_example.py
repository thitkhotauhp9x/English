import os.path
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.wrappers import trace


@trace()
def add(a: int, b: int) -> int:
    return a + b


@trace()
def real_path(a: Path) -> str:
    return a.absolute().as_posix()


def main():
    add(1, 2)
    add(1, b=2)
    add(a=1, b=2)

    with NamedTemporaryFile() as temp_file:
        temp_path = Path(temp_file.name)
        temp_path.write_bytes(b"...")
        os.path.getsize(temp_path)
        real_path(temp_path)


if __name__ == "__main__":
    main()
