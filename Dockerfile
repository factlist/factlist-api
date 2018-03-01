FROM python:3.5.2

COPY requirements.txt ./
RUN pip install -r requirements.txt
