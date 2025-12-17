FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем только то, что нужно приложению
COPY src /app/src
COPY data /app/data
COPY logs /app/logs

# Устанавливаем зависимости
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir customtkinter

# Говорим Python, где корень проекта
ENV PYTHONPATH=/app/src

# Точка входа приложения
CMD ["python", "-m", "task_manager.main"]
