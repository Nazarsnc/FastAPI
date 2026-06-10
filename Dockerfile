FROM python:3.11-slim

WORKDIR /app

# Встановлюємо системні залежності
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/list/apt/lists/*

# Встановлюємо Poetry
RUN pip install --no-cache-dir poetry

# Вимикаємо створення віртуальних середовищ всередині контейнера
RUN poetry config virtualenvs.create false

# Копіюємо конфіги залежностей
COPY pyproject.toml poetry.lock* ./

# Встановлюємо залежності проєкту
RUN poetry install --no-interaction --no-ansi --no-root

# Копіюємо всю папку app в контейнер
COPY ./app ./app

# Зміна 1: Копіюємо нашу офіційну точку входу в контейнер
COPY ./run.py ./run.py

# Зміна 2: Запускаємо додаток НЕ через uvicorn напряму, а ЧЕРЕЗ ТОЧКУ ВХОДУ Python
CMD ["python", "run.py"]