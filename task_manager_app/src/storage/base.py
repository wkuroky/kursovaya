from abc import ABC, abstractmethod
from core.models import Task


class BaseStorage(ABC):
    @abstractmethod
    def load(self) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def save(self, tasks: list[Task]) -> None:
        raise NotImplementedError
