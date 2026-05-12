FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry==1.8.3
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi --verbose
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]


#FROM python:3.13-slim
#
#ENV PYTHONUNBUFFERED=1
#ENV PYTHONNOBYTECODE=1
#
#WORKDIR /app
#
#RUN apt-get update && apt-get install -y gcc python3-dev build-essential && rm -rf /var/lib/apt/lists/*
#RUN apt-get update && apt-get install -y \
#    gcc \
#    python3-dev \
#    build-essential \
#    libpq-dev \
#    libjpeg-dev \
#    zlib1g-dev && \
#    rm -rf /var/lib/apt/lists/*
#RUN pip install --upgrade pip
#RUN pip install poetry==1.8.3
#RUN echo '[tool.poetry]' > pyproject.toml && \
#    echo 'name = "test"' >> pyproject.toml && \
#    echo 'version = "0.1.0"' >> pyproject.toml && \
#    echo '[tool.poetry.dependencies]' >> pyproject.toml && \
#    echo 'python = "^3.13"' >> pyproject.toml
#RUN poetry config virtualenvs.create false --local
#RUN poetry config installer.parallel false
#COPY pyproject.toml poetry.lock ./
#RUN set -x && \
#    poetry install --no-interaction --no-ansi --verbose 2>&1 | tee poetry-install.log && \
#    set +x
#RUN poetry install --no-interaction --no-ansi --verbose
#RUN rm -rf ~/.cache/pypoetry
#COPY . .
#RUN python -c "import django; print(f'Django {django.get_version()} успешно установлен')"
#CMD ["echo", "Poetry работает!"]
#CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]