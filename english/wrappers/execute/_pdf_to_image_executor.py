from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from english.wrappers.execute._base_executor import BaseExecutor


@dataclass
class PdfToImageExecutor(BaseExecutor):
    path: Path
    density: int = field(default=300)

    @property
    def args(self) -> List[str]:
        return [
            "convert",
            "-density",
            str(self.density),
            "-trim",
            self.path.as_posix(),
            "-quality",
            str(100),
            "test.jpg",
        ]
