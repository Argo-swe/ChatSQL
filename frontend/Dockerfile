# base image
FROM node:20.14.0

# bind your app to the gateway IP
ENV HOST=0.0.0.0

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY vite.config.ts ./
COPY package*.json ./

RUN npm ci

# Bundle app source
COPY . .

EXPOSE 8080

CMD [ "npm", "run", "dev"]
