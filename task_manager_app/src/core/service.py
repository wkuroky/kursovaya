from core.models import Task


class TaskService:
    def __init__(self):
        self._tasks: list[Task] = []

    def seed_demo(self):
        if self._tasks:
            return
        self.add_task("Купить продукты", "Молоко, хлеб, яйца", "2025-01-10")
        self.add_task("Сделать курсовую", "UI + JSON + логи", "2025-02-01")
        self.add_task("Погулять", "30 минут вечером", "")

    def add_task(self, title: str, description: str = "", due_date: str = "") -> Task:
        task = Task(title=title.strip() or "Без названия", description=description, due_date=due_date)
        self._tasks.append(task)
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
        return len(self._tasks) != before

    def update_task(self, task_id: str, title: str, description: str, due_date: str, status: str) -> bool:
        t = self.get_task(task_id)
        if not t:
            return False
        t.title = title.strip() or "Без названия"
        t.description = description
        t.due_date = due_date
        t.status = status
        return True

    def mark_done(self, task_id: str) -> bool:
        t = self.get_task(task_id)
        if not t:
            return False
        t.status = "done"
        return True
