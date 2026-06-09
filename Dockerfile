FROM python:3.10-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Забороняємо Python писати файли .pyc та вмикаємо буферизацію логів
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Встановлюємо Poetry
RUN pip install --no-cache-dir poetry

# Вимикаємо створення віртуальних середовищ всередині контейнера (Poetry ставитиме все системно)
RUN poetry config virtualenvs.create false

# Копіюємо конфігураційні файли Poetry
COPY pyproject.toml poetry.lock* /app/

# Встановлюємо залежності проєкту
RUN poetry install --no-interaction --no-ansi --no-root

# Копіюємо код проєкту
COPY src /app/src
COPY README.md /app/

# Запуск сервера (для прод-версії без автоперезавантаження)
CMD ["uvicorn", "fastapi_template.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]