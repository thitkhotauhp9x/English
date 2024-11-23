from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Generator


@dataclass
class File:
    path: Path

    @contextmanager
    def write_temporary_file(self, directory: Path) -> Generator[Path, None, None]:
        with NamedTemporaryFile(suffix=self.path.suffix, dir=directory) as temp_file:
            temp_path: Path = Path(temp_file.name)
            temp_path.write_bytes(self.path.read_bytes())
            yield temp_path

    @property
    def suffix(self) -> str:
        return self.path.suffix
