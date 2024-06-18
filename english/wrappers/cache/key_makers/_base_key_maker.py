import hashlib
import pickle
from abc import ABC, abstractmethod


class BaseKeyMaker(ABC):
    @abstractmethod
    def make(self) -> tuple:
        raise NotImplementedError()

    def hash(self):
        return hashlib.sha256(pickle.dumps(self.make())).hexdigest()
