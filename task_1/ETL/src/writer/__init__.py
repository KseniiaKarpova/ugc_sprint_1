from abc import ABC, abstractmethod
from typing import Any


class AbstractWriter(ABC):

    @abstractmethod
    def write(self, data: list[Any]):
        pass
