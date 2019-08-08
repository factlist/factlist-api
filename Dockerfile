FROM node:alpine
WORKDIR /
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 4000
CMD ["npm", "run", "docker"]
