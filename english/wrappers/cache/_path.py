import pickle
from pathlib import Path


def encode(path: Path) -> bytes:
    return pickle.dumps((path.name, path.read_bytes()))


def decode(data: bytes) -> Path:
    name, content = pickle.loads(data)
    path = Path(name)
    path.write_bytes(content)
    return path
