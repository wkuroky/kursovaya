from core.models import Task
from storage.base import BaseStorage


class TaskService:
    def __init__(self, storage: BaseStorage):
        self._storage = storage
        self._tasks: list[Task] = []

    def load(self) -> None:
        self._tasks = self._storage.load()

    def save(self) -> None:
        self._storage.save(self._tasks)

    def seed_demo_if_empty(self) -> None:
        if self._tasks:
            return
        self.add_task("Купить продукты", "Молоко, хлеб, яйца", "2025-01-10", autosave=False)
        self.add_task("Сделать курсовую", "UI + JSON + логи", "2025-02-01", autosave=False)
        self.add_task("Погулять", "30 минут вечером", "", autosave=False)
        self.save()

    def add_task(self, title: str, description: str = "", due_date: str = "", autosave: bool = True) -> Task:
        task = Task(title=title.strip() or "Без названия", description=description, due_date=due_date)
        self._tasks.append(task)
        if autosave:
            self.save()
        return task

    def list_tasks(self, status: str | None = None) -> list[Task]:
        if status is None:
            return list(self._tasks)
        return [t for t in self._tasks if t.status == status]

    def get_task(self, task_id: str) -> Task | None:
        for t in self._tasks:
            if t.id == task_id:
                return t
        return None

    def delete_task(self, task_id: str) -> bool:
        before = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.id != task_id]
        changed = len(self._tasks) != before
        if changed:
            self.save()
        return changed

    def update_task(self, task_id: str, title: str, description: str, due_date: str, status: str) -> bool:
        t = self.get_task(task_id)
        if not t:
            return False
        t.title = title.strip() or "Без названия"
        t.description = description
        t.due_date = due_date
        t.status = status
        self.save()
        return True

    def mark_done(self, task_id: str) -> bool:
        t = self.get_task(task_id)
        if not t:
            return False
        t.status = "done"
        self.save()
        return True
