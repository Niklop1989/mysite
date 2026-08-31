#FROM python:3.13

#ENV PYTHONUNBUFFERED=1

#RUN mkdir /app

#COPY requirements.txt /app/

#COPY mysite /app/

#RUN pip install -r /app/requirements.txt

#WORKDIR /app

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["python", "manage.py", "runserver"]

# docker build -t app .
# docker run -p 8000:8000 app


##########################################################################
# docker-compose
#####################################################################

# с docker-compose

FROM python:3.13

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY mysite .

#CMD ["python", "manage.py", "runserver"]
CMD ["gunicorn","mysite.wsgi:application","--bind","0.0.0.0:8080"]

