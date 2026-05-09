FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ../requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY static/ /app/static/
COPY .. .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]