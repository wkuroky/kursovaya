import customtkinter as ctk
from datetime import datetime

from core.service import TaskService
from storage.json_storage import JsonStorage
from ui.views import SidebarView, TaskListView, TaskDetailsView
from ui.dialogs import NewTaskDialog, MessageDialog, ConfirmDialog, SettingsDialog
from utils.logging_conf import setup_logging
from utils.settings import Settings


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.logger = setup_logging()

        # Настройки
        self.settings = Settings("data/settings.json")
        self.settings.load()
        ctk.set_appearance_mode(self.settings.appearance_mode)
        ctk.set_default_color_theme("blue")

        self.title("Task Manager")
        self.geometry("1100x650")
        self.minsize(950, 550)

        self.storage = JsonStorage("data/tasks.json")
        self.service = TaskService(self.storage)
        self.service.load()
        self.service.seed_demo_if_empty()

        self.selected_id: str | None = None
        self.current_filter: str | None = None  # None / "active" / "done"
        self.search_query: str = ""

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = SidebarView(self)
        self.sidebar.grid(row=0, column=0, sticky="nsw", padx=(10, 5), pady=10)

        self.list_view = TaskListView(self)
        self.list_view.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)

        self.details_view = TaskDetailsView(self)
        self.details_view.grid(row=0, column=2, sticky="nsew", padx=(5, 10), pady=10)

        # callbacks
        self.list_view.on_select = self.on_select_task
        self.list_view.on_search = self.on_search

        self.sidebar.btn_all.configure(command=self.show_all)
        self.sidebar.btn_active.configure(command=self.show_active)
        self.sidebar.btn_done.configure(command=self.show_done)
        self.sidebar.btn_new.configure(command=self.create_task)
        self.sidebar.btn_settings.configure(command=self.open_settings)
        self.sidebar.btn_exit.configure(command=self.destroy)

        self.details_view.btn_save.configure(command=self.save_selected)
        self.details_view.btn_delete.configure(command=self.delete_selected)
        self.details_view.btn_done.configure(command=self.mark_selected_done)

        self.show_all()

    def _is_valid_date(self, s: str) -> bool:
        s = (s or "").strip()
        if s == "":
            return True
        try:
            datetime.strptime(s, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def open_settings(self):
        dlg = SettingsDialog(self, self.settings.appearance_mode, self.settings.autosave)
        self.wait_window(dlg)
        if not dlg.result:
            return

        mode, autosave = dlg.result
        self.settings.appearance_mode = mode
        self.settings.autosave = autosave
        self.settings.save()

        ctk.set_appearance_mode(mode)
        MessageDialog(self, "Настройки", "Настройки сохранены.\nТема применена сразу.")

    def update_stats(self):
        st = self.service.stats()
        self.sidebar.set_stats(st["total"], st["active"], st["done"])

    def apply_filters(self, tasks):
        q = (self.search_query or "").strip().lower()
        if q:
            tasks = [
                t for t in tasks
                if q in (t.title or "").lower() or q in (t.description or "").lower()
            ]

        # сортировка по приоритету (high > medium > low)
        pr_rank = {"high": 3, "medium": 2, "low": 1}
        tasks.sort(key=lambda t: pr_rank.get(t.priority, 2), reverse=True)
        return tasks

    def refresh(self):
        if self.current_filter is None:
            tasks = self.service.list_tasks()
        else:
            tasks = self.service.list_tasks(self.current_filter)

        tasks = self.apply_filters(tasks)
        self.list_view.render(tasks)
        self.update_stats()

    def on_search(self, query: str):
        self.search_query = query
        self.refresh()

    def show_all(self):
        self.current_filter = None
        self.refresh()

    def show_active(self):
        self.current_filter = "active"
        self.refresh()

    def show_done(self):
        self.current_filter = "done"
        self.refresh()

    def on_select_task(self, task_id: str):
        self.selected_id = task_id
        task = self.service.get_task(task_id)
        if not task:
            return

        self.details_view.title_entry.delete(0, "end")
        self.details_view.title_entry.insert(0, task.title)

        self.details_view.desc_box.delete("1.0", "end")
        self.details_view.desc_box.insert("1.0", task.description)

        self.details_view.due_entry.delete(0, "end")
        self.details_view.due_entry.insert(0, task.due_date)

        self.details_view.status_menu.set(task.status)
        self.details_view.priority_menu.set(task.priority)

    def create_task(self):
        dlg = NewTaskDialog(self)
        self.wait_window(dlg)
        if not dlg.result:
            return

        title, desc, due, pr = dlg.result

        task = self.service.add_task(
            title, desc, due, pr,
            autosave=self.settings.autosave
        )

        if not self.settings.autosave:
            # если автосохранение выключено — сохраняем только при явной необходимости (пока оставим как есть)
            pass

        self.refresh()
        self.on_select_task(task.id)

    def save_selected(self):
        if not self.selected_id:
            MessageDialog(self, "Ошибка", "Сначала выберите задачу в списке.")
            return

        title = self.details_view.title_entry.get().strip()
        desc = self.details_view.desc_box.get("1.0", "end").strip()
        due = self.details_view.due_entry.get().strip()
        status = self.details_view.status_menu.get()
        pr = self.details_view.priority_menu.get()

        if title == "":
            MessageDialog(self, "Ошибка", "Название задачи не может быть пустым.")
            return

        if not self._is_valid_date(due):
            MessageDialog(self, "Ошибка", "Неверная дата.\nВведите в формате YYYY-MM-DD, например 2025-12-31.")
            return

        ok = self.service.update_task(
            self.selected_id, title, desc, due, status, pr,
            autosave=self.settings.autosave
        )
        if ok:
            self.refresh()

    def delete_selected(self):
        if not self.selected_id:
            MessageDialog(self, "Ошибка", "Сначала выберите задачу в списке.")
            return

        task = self.service.get_task(self.selected_id)
        title = task.title if task else "эту задачу"

        dlg = ConfirmDialog(self, "Подтверждение", f"Удалить задачу:\n\n{title}\n\n?")
        self.wait_window(dlg)
        if not dlg.result:
            return

        ok = self.service.delete_task(self.selected_id, autosave=self.settings.autosave)
        if ok:
            self.selected_id = None
            self.refresh()

    def mark_selected_done(self):
        if not self.selected_id:
            MessageDialog(self, "Ошибка", "Сначала выберите задачу в списке.")
            return

        ok = self.service.mark_done(self.selected_id, autosave=self.settings.autosave)
        if ok:
            self.refresh()
