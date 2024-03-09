from abc import ABC, abstractmethod
from typing import Any


class AbstractReader(ABC):
    """Абстрактный класс для подключения к хранилищу."""

    @abstractmethod
    def read_data(self) -> list[Any]:
        pass

    @abstractmethod
    def commit(self):
        pass
