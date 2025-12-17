import json
from pathlib import Path


class Settings:
    def __init__(self, path: str = "data/settings.json"):
        self.path = Path(path)
        self.appearance_mode = "System"  # "Light" | "Dark" | "System"
        self.autosave = True            # автосохранение в JSON

    def load(self):
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.appearance_mode = data.get("appearance_mode", self.appearance_mode)
            self.autosave = bool(data.get("autosave", self.autosave))
        except Exception:
            # если файл битый — просто оставляем дефолты
            return

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "appearance_mode": self.appearance_mode,
            "autosave": self.autosave,
        }
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
