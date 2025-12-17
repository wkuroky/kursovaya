import customtkinter as ctk
from datetime import datetime


class MessageDialog(ctk.CTkToplevel):
    def __init__(self, master, title: str, message: str):
        super().__init__(master)
        self.title(title)
        self.geometry("420x170")
        self.resizable(False, False)

        self.grab_set()
        self.lift()
        self.focus_force()

        ctk.CTkLabel(self, text=message, justify="left", wraplength=380).pack(padx=20, pady=(25, 15))
        ctk.CTkButton(self, text="OK", command=self.destroy).pack(pady=(0, 20))

        self.update_idletasks()


class NewTaskDialog(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Новая задача")
        self.minsize(420, 420)
        self.geometry("420x420")
        self.resizable(False, False)

        self.result = None  # (title, desc, due)

        self.grab_set()
        self.lift()
        self.focus_force()

        ctk.CTkLabel(self, text="Название").pack(anchor="w", padx=15, pady=(15, 5))
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Например: Сделать курсовую")
        self.title_entry.pack(fill="x", padx=15)

        ctk.CTkLabel(self, text="Описание").pack(anchor="w", padx=15, pady=(12, 5))
        self.desc_box = ctk.CTkTextbox(self, height=160)
        self.desc_box.pack(fill="both", expand=True, padx=15)

        ctk.CTkLabel(self, text="Срок (YYYY-MM-DD)").pack(anchor="w", padx=15, pady=(12, 5))

        vcmd = (self.register(self._validate_date_input), "%P")
        self.due_entry = ctk.CTkEntry(
            self,
            placeholder_text="2025-12-31",
            validate="key",
            validatecommand=vcmd
        )
        self.due_entry.pack(fill="x", padx=15)

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=15, pady=15)
        btns.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btns, text="Создать", command=self._ok).grid(row=0, column=0, padx=(0, 8), sticky="ew")
        ctk.CTkButton(btns, text="Отмена", command=self._cancel).grid(row=0, column=1, padx=(8, 0), sticky="ew")

        self.update_idletasks()

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

    def _is_valid_date(self, s: str) -> bool:
        s = (s or "").strip()
        if s == "":
            return True
        try:
            datetime.strptime(s, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _ok(self):
        title = self.title_entry.get().strip()
        desc = self.desc_box.get("1.0", "end").strip()
        due = self.due_entry.get().strip()

        if title == "":
            MessageDialog(self, "Ошибка", "Название задачи не может быть пустым.")
            return

        if not self._is_valid_date(due):
            MessageDialog(self, "Ошибка", "Неверная дата.\nВведите в формате YYYY-MM-DD, например 2025-12-31.")
            return

        self.result = (title, desc, due)
        self.destroy()

    def _cancel(self):
        self.result = None
        self.destroy()
