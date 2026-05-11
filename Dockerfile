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
