import json
from pathlib import Path

from core.models import Task
from storage.base import BaseStorage


class JsonStorage(BaseStorage):
    def __init__(self, filepath: str):
        self.path = Path(filepath)

    def load(self) -> list[Task]:
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return []

        return [Task.from_dict(item) for item in data if isinstance(item, dict)]

    def save(self, tasks: list[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = [t.to_dict() for t in tasks]
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
