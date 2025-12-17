from core.models import Task
from storage.base import BaseStorage


class MemoryStorage(BaseStorage):
    def __init__(self):
        self._tasks: list[Task] = []

    def load(self) -> list[Task]:
        return list(self._tasks)

    def save(self, tasks: list[Task]) -> None:
        self._tasks = list(tasks)
