import customtkinter as ctk

from core.service import TaskService
from ui.views import SidebarView, TaskListView, TaskDetailsView


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

        # связки
        self.list_view.on_select = self.on_select_task

        self.sidebar.btn_all.configure(command=self.show_all)
        self.sidebar.btn_active.configure(command=self.show_active)
        self.sidebar.btn_done.configure(command=self.show_done)
        self.sidebar.btn_exit.configure(command=self.destroy)

        # пока просто отображаем всё
        self.show_all()

    def show_all(self):
        self.list_view.render(self.service.list_tasks())

    def show_active(self):
        self.list_view.render(self.service.list_tasks("active"))

    def show_done(self):
        self.list_view.render(self.service.list_tasks("done"))

    def on_select_task(self, task_id: str):
        self.selected_id = task_id
        task = self.service.get_task(task_id)
        if not task:
            return
        # заполним панель деталей (чуть позже добавим кнопки "сохранить/удалить")
        self.details_view.title_entry.delete(0, "end")
        self.details_view.title_entry.insert(0, task.title)

        self.details_view.desc_box.delete("1.0", "end")
        self.details_view.desc_box.insert("1.0", task.description)

        self.details_view.due_entry.delete(0, "end")
        self.details_view.due_entry.insert(0, task.due_date)

        self.details_view.status_menu.set(task.status)
