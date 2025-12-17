from core.service import TaskService
from .fakes import MemoryStorage





def make_service():
    storage = MemoryStorage()
    service = TaskService(storage)
    service.load()
    return service


def test_add_task_creates_task_and_persists():
    svc = make_service()
    t = svc.add_task("Read book", "Chapter 1", "2025-12-31")

    tasks = svc.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == t.id
    assert tasks[0].title == "Read book"


def test_update_task_changes_fields():
    svc = make_service()
    t = svc.add_task("Old", "desc", "2025-01-01")

    ok = svc.update_task(t.id, "New", "new desc", "2025-02-02", "active")
    assert ok is True

    updated = svc.get_task(t.id)
    assert updated is not None
    assert updated.title == "New"
    assert updated.description == "new desc"
    assert updated.due_date == "2025-02-02"
    assert updated.status == "active"


def test_delete_task_removes_task():
    svc = make_service()
    t = svc.add_task("To delete", "", "")

    ok = svc.delete_task(t.id)
    assert ok is True
    assert svc.get_task(t.id) is None
    assert svc.list_tasks() == []


def test_mark_done_sets_status_done():
    svc = make_service()
    t = svc.add_task("Do it", "", "")

    ok = svc.mark_done(t.id)
    assert ok is True
    assert svc.get_task(t.id).status == "done"


def test_list_tasks_filters_by_status():
    svc = make_service()
    a = svc.add_task("A", "", "")
    b = svc.add_task("B", "", "")

    svc.mark_done(b.id)

    active = svc.list_tasks("active")
    done = svc.list_tasks("done")

    assert len(active) == 1 and active[0].id == a.id
    assert len(done) == 1 and done[0].id == b.id


def test_update_nonexistent_returns_false():
    svc = make_service()
    ok = svc.update_task("no-such-id", "x", "y", "", "active")
    assert ok is False


def test_delete_nonexistent_returns_false():
    svc = make_service()
    ok = svc.delete_task("no-such-id")
    assert ok is False
