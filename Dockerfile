<<<<<<< HEAD
FROM python:3.5.2

RUN mkdir /api
WORKDIR /api
COPY requirements.txt ./
RUN pip install -r requirements.txt
ADD . /api/

EXPOSE 8000
=======
FROM node:alpine
WORKDIR "/app"
COPY ./package.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "docker"]
>>>>>>> develop
