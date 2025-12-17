import customtkinter as ctk

from ui.views import SidebarView, TaskListView, TaskDetailsView


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title("Task Manager")
        self.geometry("1100x650")
        self.minsize(950, 550)

        # Сетка: 3 колонки (лево / центр / право)
        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # list
        self.grid_columnconfigure(2, weight=1)  # details
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = SidebarView(self)
        self.sidebar.grid(row=0, column=0, sticky="nsw", padx=(10, 5), pady=10)

        self.list_view = TaskListView(self)
        self.list_view.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)

        self.details_view = TaskDetailsView(self)
        self.details_view.grid(row=0, column=2, sticky="nsew", padx=(5, 10), pady=10)
