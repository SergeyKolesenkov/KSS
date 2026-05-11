#FROM python:3.13-slim
#
#ENV PYTHONUNBUFFERED=1
#
#WORKDIR /app
#
#RUN pip install --upgrade pip
#RUN pip install poetry
#RUN poetry config virtualenvs.create false --local
#COPY pyproject.toml poetry.lock ./
#RUN poetry install --no-interaction --no-ansi --verbose
#COPY static/ /app/static/
#COPY staticfiles/ /app/staticfiles/
#COPY .. .
#RUN python manage.py collectstatic --noinput
#CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
FROM python:3.13-slim

WORKDIR /app

# Установка зависимостей
RUN apt-get update && apt-get install -y gcc python3-dev build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install poetry==1.8.3

# Создаём минимальный pyproject.toml прямо в Dockerfile
RUN echo '[tool.poetry]' > pyproject.toml && \
    echo 'name = "test"' >> pyproject.toml && \
    echo 'version = "0.1.0"' >> pyproject.toml && \
    echo '[tool.poetry.dependencies]' >> pyproject.toml && \
    echo 'python = "^3.13"' >> pyproject.toml

# Пробуем установить зависимости
RUN poetry install --no-interaction --no-ansi --verbose


CMD ["echo", "Poetry работает!"]