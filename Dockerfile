FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip 'poetry=2.4.1'
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY static/ /app/static/
COPY staticfiles/ /app/staticfiles/
COPY .. .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]