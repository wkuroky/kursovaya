import customtkinter as ctk


class SidebarView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=240)
        self.grid_rowconfigure(10, weight=1)

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

        # Статистика
        stat_title = ctk.CTkLabel(self, text="Статистика", font=("Arial", 14, "bold"))
        stat_title.grid(row=5, column=0, padx=15, pady=(20, 5), sticky="w")

        self.lbl_total = ctk.CTkLabel(self, text="Всего: 0")
        self.lbl_total.grid(row=6, column=0, padx=15, pady=2, sticky="w")

        self.lbl_active = ctk.CTkLabel(self, text="Активных: 0")
        self.lbl_active.grid(row=7, column=0, padx=15, pady=2, sticky="w")

        self.lbl_done = ctk.CTkLabel(self, text="Выполнено: 0")
        self.lbl_done.grid(row=8, column=0, padx=15, pady=2, sticky="w")

        self.btn_settings = ctk.CTkButton(self, text="⚙ Настройки")
        self.btn_settings.grid(row=11, column=0, padx=15, pady=(5, 5), sticky="ew")

        self.btn_exit = ctk.CTkButton(self, text="Выход")
        self.btn_exit.grid(row=12, column=0, padx=15, pady=(5, 15), sticky="ew")

    def set_stats(self, total: int, active: int, done: int):
        self.lbl_total.configure(text=f"Всего: {total}")
        self.lbl_active.configure(text=f"Активных: {active}")
        self.lbl_done.configure(text=f"Выполнено: {done}")


class TaskListView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.on_select = None    # callback(task_id)
        self.on_search = None    # callback(query)

        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header.grid_columnconfigure(0, weight=1)

        self.search = ctk.CTkEntry(header, placeholder_text="Поиск по названию/описанию...")
        self.search.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=10)
        self.search.bind("<KeyRelease>", self._handle_search)

        self.sort = ctk.CTkOptionMenu(header, values=["Сортировка: по приоритету", "Сортировка: по статусу"])
        self.sort.grid(row=0, column=1, sticky="e", pady=10)

        self.body = ctk.CTkScrollableFrame(self)
        self.body.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

    def _handle_search(self, _event=None):
        if self.on_search:
            self.on_search(self.search.get())

    def render(self, tasks):
        for w in self.body.winfo_children():
            w.destroy()

        for t in tasks:
            card = ctk.CTkFrame(self.body)
            card.pack(fill="x", padx=5, pady=6)

            pr_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(t.priority, "🟡")
            title = ctk.CTkLabel(card, text=f"{pr_icon} {t.title}", font=("Arial", 15, "bold"))
            title.pack(anchor="w", padx=10, pady=(10, 0))

            status = "✅ done" if t.status == "done" else "🟦 active"
            meta = ctk.CTkLabel(card, text=f"{status}   Срок: {t.due_date or '-'}   Приоритет: {t.priority}")
            meta.pack(anchor="w", padx=10, pady=(2, 0))

            short_desc = (t.description[:60] + "…") if len(t.description) > 60 else t.description
            desc = ctk.CTkLabel(card, text=short_desc)
            desc.pack(anchor="w", padx=10, pady=(2, 10))

            def _select(_event=None, task_id=t.id):
                if self.on_select:
                    self.on_select(task_id)

            for w in (card, title, meta, desc):
                w.bind("<Button-1>", _select)


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

        vcmd = (self.register(self._validate_date_input), "%P")
        self.due_entry = ctk.CTkEntry(
            self,
            placeholder_text="Срок (например 2025-12-31)",
            validate="key",
            validatecommand=vcmd
        )
        self.due_entry.grid(row=3, column=0, padx=15, pady=8, sticky="ew")

        self.status_menu = ctk.CTkOptionMenu(self, values=["active", "done"])
        self.status_menu.grid(row=4, column=0, padx=15, pady=8, sticky="w")

        ctk.CTkLabel(self, text="Приоритет").grid(row=5, column=0, padx=15, pady=(8, 2), sticky="w")
        self.priority_menu = ctk.CTkOptionMenu(self, values=["low", "medium", "high"])
        self.priority_menu.grid(row=6, column=0, padx=15, pady=(0, 8), sticky="w")

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.grid(row=7, column=0, padx=15, pady=(15, 10), sticky="ew")
        btns.grid_columnconfigure((0, 1), weight=1)

        self.btn_save = ctk.CTkButton(btns, text="Сохранить")
        self.btn_save.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.btn_delete = ctk.CTkButton(btns, text="Удалить")
        self.btn_delete.grid(row=0, column=1, padx=(8, 0), sticky="ew")

        self.btn_done = ctk.CTkButton(self, text="Отметить выполненной")
        self.btn_done.grid(row=8, column=0, padx=15, pady=(5, 15), sticky="ew")

    def _validate_date_input(self, value: str) -> bool:
        if value == "":
            return True
        if len(value) > 10:
            return False
        for ch in value:
            if not (ch.isdigit() or ch == "-"):
                return False
        for i, ch in enumerate(value):
            if ch == "-" and i not in (4, 7):
                return False
        return True
