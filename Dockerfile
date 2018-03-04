FROM python:3.5.2

RUN mkdir /api
WORKDIR /api
COPY requirements.txt ./
RUN pip install -r requirements.txt
ADD . /api/
