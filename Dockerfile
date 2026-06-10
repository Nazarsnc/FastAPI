FROM python:3.11-slim

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/list/apt/lists/*


RUN pip install --no-cache-dir poetry


RUN poetry config virtualenvs.create false


COPY pyproject.toml poetry.lock* ./


RUN poetry install --no-interaction --no-ansi --no-root


COPY ./app ./app


COPY ./run.py ./run.py


CMD ["python", "run.py"]