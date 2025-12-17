import logging
from pathlib import Path


def setup_logging(log_path: str = "logs/app.log") -> logging.Logger:
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("task_manager")
    logger.setLevel(logging.INFO)

    # чтобы не дублировать хендлеры при перезапусках из IDE
    if logger.handlers:
        return logger

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(fmt)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
