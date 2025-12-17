from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Task:
    title: str
    description: str = ""
    due_date: str = ""                 # "YYYY-MM-DD" или пусто
    status: str = "active"             # "active" | "done"
    priority: str = "medium"           # "low" | "medium" | "high"
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        t = Task(
            title=data.get("title", ""),
            description=data.get("description", ""),
            due_date=data.get("due_date", ""),
            status=data.get("status", "active"),
            priority=data.get("priority", "medium"),
        )
        t.id = data.get("id", t.id)
        t.created_at = data.get("created_at", t.created_at)
        return t
