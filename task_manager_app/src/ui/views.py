import customtkinter as ctk


class SidebarView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=220)
        self.grid_rowconfigure(6, weight=1)

        title = ctk.CTkLabel(self, text="Task Manager", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")

        self.btn_all = ctk.CTkButton(self, text="Все задачи")
        self.btn_all.grid(row=1, column=0, padx=15, pady=5, sticky="ew")

        self.btn_active = ctk.CTkButton(self, text="Активные")
        self.btn_active.grid(row=2, column=0, padx=15, pady=5, sticky="ew")

        self.btn_done = ctk.CTkButton(self, text="Выполненные")
        self.btn_done.grid(row=3, column=0, padx=15, pady=5, sticky="ew")

        self.btn_new = ctk.CTkButton(self, text="+ Новая задача")
        self.btn_new.grid(row=4, column=0, padx=15, pady=(15, 5), sticky="ew")

        self.btn_exit = ctk.CTkButton(self, text="Выход")
        self.btn_exit.grid(row=7, column=0, padx=15, pady=15, sticky="ew")


class TaskListView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header.grid_columnconfigure(0, weight=1)

        self.search = ctk.CTkEntry(header, placeholder_text="Поиск по задачам...")
        self.search.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=10)

        self.sort = ctk.CTkOptionMenu(header, values=["Сортировка: по дате", "Сортировка: по статусу"])
        self.sort.grid(row=0, column=1, sticky="e", pady=10)

        # Список (пока заглушки-карточки)
        body = ctk.CTkScrollableFrame(self)
        body.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        for i in range(1, 8):
            card = ctk.CTkFrame(body)
            card.pack(fill="x", padx=5, pady=6)

            title = ctk.CTkLabel(card, text=f"Задача #{i}: пример", font=("Arial", 15, "bold"))
            title.pack(anchor="w", padx=10, pady=(10, 0))

            desc = ctk.CTkLabel(card, text="Короткое описание задачи (пока заглушка)...")
            desc.pack(anchor="w", padx=10, pady=(2, 10))


class TaskDetailsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Детали задачи", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")

        self.title_entry = ctk.CTkEntry(self, placeholder_text="Название")
        self.title_entry.grid(row=1, column=0, padx=15, pady=8, sticky="ew")

        self.desc_box = ctk.CTkTextbox(self, height=180)
        self.desc_box.grid(row=2, column=0, padx=15, pady=8, sticky="ew")
        self.desc_box.insert("1.0", "Описание задачи...")

        self.due_entry = ctk.CTkEntry(self, placeholder_text="Срок (например 2025-12-31)")
        self.due_entry.grid(row=3, column=0, padx=15, pady=8, sticky="ew")

        self.status_menu = ctk.CTkOptionMenu(self, values=["active", "done"])
        self.status_menu.grid(row=4, column=0, padx=15, pady=8, sticky="w")

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.grid(row=5, column=0, padx=15, pady=(15, 10), sticky="ew")
        btns.grid_columnconfigure((0, 1), weight=1)

        self.btn_save = ctk.CTkButton(btns, text="Сохранить")
        self.btn_save.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.btn_delete = ctk.CTkButton(btns, text="Удалить")
        self.btn_delete.grid(row=0, column=1, padx=(8, 0), sticky="ew")

        self.btn_done = ctk.CTkButton(self, text="Отметить выполненной")
        self.btn_done.grid(row=6, column=0, padx=15, pady=(5, 15), sticky="ew")
