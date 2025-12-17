from core.models import Task
from storage.base import BaseStorage
from utils.logging_conf import setup_logging


logger = setup_logging()


class TaskService:
    def __init__(self, storage: BaseStorage):
        self._storage = storage
        self._tasks: list[Task] = []
        logger.info("TaskService initialized")

    def load(self) -> None:
        self._tasks = self._storage.load()
        logger.info("Service load: %d tasks in memory", len(self._tasks))

    def save(self) -> None:
        self._storage.save(self._tasks)

    def seed_demo_if_empty(self) -> None:
        if self._tasks:
            return
        logger.info("Seeding demo tasks (storage empty)")
        self.add_task("Купить продукты", "Молоко, хлеб, яйца", "2025-01-10", "medium", autosave=False)
        self.add_task("Сделать курсовую", "UI + JSON + логи + тесты + Docker", "2025-02-01", "high", autosave=False)
        self.add_task("Погулять", "30 минут вечером", "", "low", autosave=False)
        self.save()

    def add_task(self, title: str, description: str = "", due_date: str = "", priority: str = "medium", autosave: bool = True) -> Task:
        priority = priority if priority in ("low", "medium", "high") else "medium"
        task = Task(title=title.strip() or "Без названия", description=description, due_date=due_date, priority=priority)
        self._tasks.append(task)
        logger.info("Task created: id=%s title=%r priority=%s", task.id, task.title, task.priority)
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

    def delete_task(self, task_id: str, autosave: bool = True) -> bool:
        t = self.get_task(task_id)
        before = len(self._tasks)
        self._tasks = [x for x in self._tasks if x.id != task_id]
        changed = len(self._tasks) != before
        if changed:
            logger.info("Task deleted: id=%s title=%r", task_id, (t.title if t else None))
            if autosave:
                self.save()
        else:
            logger.warning("Task delete failed (not found): id=%s", task_id)
        return changed

    def update_task(self, task_id: str, title: str, description: str, due_date: str, status: str, priority: str, autosave: bool = True) -> bool:
        t = self.get_task(task_id)
        if not t:
            logger.warning("Task update failed (not found): id=%s", task_id)
            return False

        t.title = title.strip() or "Без названия"
        t.description = description
        t.due_date = due_date
        t.status = status
        t.priority = priority if priority in ("low", "medium", "high") else "medium"

        logger.info("Task updated: id=%s title=%r status=%s priority=%s", t.id, t.title, t.status, t.priority)
        if autosave:
            self.save()
        return True

    def mark_done(self, task_id: str, autosave: bool = True) -> bool:
        t = self.get_task(task_id)
        if not t:
            logger.warning("Task mark_done failed (not found): id=%s", task_id)
            return False
        t.status = "done"
        logger.info("Task marked done: id=%s title=%r", t.id, t.title)
        if autosave:
            self.save()
        return True

    def stats(self) -> dict:
        total = len(self._tasks)
        done = sum(1 for t in self._tasks if t.status == "done")
        active = total - done
        return {"total": total, "active": active, "done": done}
