FROM python:3.13

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY mysite .

# CMD ["python", "manage.py", "runserver"]
CMD ["gunicorn","mysite.wsgi:application","--bind","0.0.0.0:8080"]

