import json
from pathlib import Path

from core.models import Task
from storage.base import BaseStorage
from utils.logging_conf import setup_logging


logger = setup_logging()


class JsonStorage(BaseStorage):
    def __init__(self, filepath: str):
        self.path = Path(filepath)

    def load(self) -> list[Task]:
        if not self.path.exists():
            logger.info("JSON load: file not found (%s) -> empty list", self.path)
            return []

        try:
            with self.path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logger.exception("JSON load: failed to read/parse %s: %s", self.path, e)
            return []

        if not isinstance(data, list):
            logger.warning("JSON load: invalid format (expected list) in %s", self.path)
            return []

        tasks = [Task.from_dict(item) for item in data if isinstance(item, dict)]
        logger.info("JSON load: loaded %d tasks from %s", len(tasks), self.path)
        return tasks

    def save(self, tasks: list[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = [t.to_dict() for t in tasks]
        try:
            with self.path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info("JSON save: saved %d tasks to %s", len(tasks), self.path)
        except Exception as e:
            logger.exception("JSON save: failed to write %s: %s", self.path, e)
