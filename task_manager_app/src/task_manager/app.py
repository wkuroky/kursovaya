import customtkinter as ctk
from datetime import datetime

from core.service import TaskService
from ui.views import SidebarView, TaskListView, TaskDetailsView
from ui.dialogs import NewTaskDialog, MessageDialog


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title("Task Manager")
        self.geometry("1100x650")
        self.minsize(950, 550)

        self.service = TaskService()
        self.service.seed_demo()
        self.selected_id: str | None = None

        self.current_filter: str | None = None  # None / "active" / "done"

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

        self.list_view.on_select = self.on_select_task

        self.sidebar.btn_all.configure(command=self.show_all)
        self.sidebar.btn_active.configure(command=self.show_active)
        self.sidebar.btn_done.configure(command=self.show_done)
        self.sidebar.btn_new.configure(command=self.create_task)
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

    def refresh(self):
        if self.current_filter is None:
            self.list_view.render(self.service.list_tasks())
        else:
            self.list_view.render(self.service.list_tasks(self.current_filter))

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

    def create_task(self):
        dlg = NewTaskDialog(self)
        self.wait_window(dlg)

        if not dlg.result:
            return

        title, desc, due = dlg.result
        task = self.service.add_task(title, desc, due)
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

        if title == "":
            MessageDialog(self, "Ошибка", "Название задачи не может быть пустым.")
            return

        if not self._is_valid_date(due):
            MessageDialog(self, "Ошибка", "Неверная дата.\nВведите в формате YYYY-MM-DD, например 2025-12-31.")
            return

        ok = self.service.update_task(self.selected_id, title, desc, due, status)
        if ok:
            self.refresh()

    def delete_selected(self):
        if not self.selected_id:
            MessageDialog(self, "Ошибка", "Сначала выберите задачу в списке.")
            return
        ok = self.service.delete_task(self.selected_id)
        if ok:
            self.selected_id = None
            self.clear_details()
            self.refresh()

    def mark_selected_done(self):
        if not self.selected_id:
            MessageDialog(self, "Ошибка", "Сначала выберите задачу в списке.")
            return
        ok = self.service.mark_done(self.selected_id)
        if ok:
            self.details_view.status_menu.set("done")
            self.refresh()

    def clear_details(self):
        self.details_view.title_entry.delete(0, "end")
        self.details_view.desc_box.delete("1.0", "end")
        self.details_view.due_entry.delete(0, "end")
        self.details_view.status_menu.set("active")
