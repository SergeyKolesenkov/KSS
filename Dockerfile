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

ENV PYTHONUNBUFFERED=1
ENV PYTHONNOBYTECODE=1

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

# Обновление pip и установка Poetry
RUN pip install --upgrade pip
RUN pip install poetry==1.8.3

# Настройка Poetry
RUN poetry config virtualenvs.create false --local
RUN poetry config installer.parallel false

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock ./

# Установка зависимостей с логированием
RUN set -x && \
    poetry install --no-interaction --no-ansi --verbose 2>&1 | tee poetry-install.log && \
    set +x

# Очистка кэша Poetry
RUN rm -rf ~/.cache/pypoetry

# Копирование кода приложения ПОСЛЕ установки зависимостей
COPY . .

# Проверка установки Django
RUN python -c "import django; print(f'Django {django.get_version()} успешно установлен')"

# Сбор статических файлов Django
#RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]]