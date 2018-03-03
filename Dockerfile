FROM python:3.5.2

RUN mkdir /api
WORKDIR /api
COPY requirements.txt ./
RUN pip install -r requirements.txt
ADD . /api/
ENTRYPOINT python manage.py runserver 0.0.0.0:8000