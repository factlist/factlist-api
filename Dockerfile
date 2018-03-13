FROM python:3.5.2

RUN mkdir /api
WORKDIR /api
COPY requirements.txt ./
COPY wait-for-it.sh ./
RUN pip install -r requirements.txt
ADD . /api/
ENTRYPOINT ./wait-for-it.sh db:3306 && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
