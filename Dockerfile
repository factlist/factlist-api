FROM node:alpine
WORKDIR /
RUN apk add --update git openssh
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 4000
CMD ["npm", "run", "docker"]
