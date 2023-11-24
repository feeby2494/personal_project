FROM node:18-alpine

WORKDIR /usr/src/app

COPY public/ /usr/src/app/public
COPY src/ /usr/src/app/src
COPY package.json /usr/src/app
COPY package-lock.json /usr/src/app
COPY .env /usr/src/app
COPY .gitignore /usr/src/app
COPY jsconfig.json /usr/src/app
COPY .env.development.local /usr/src/app

RUN npm install

CMD ["npm", "run", "start"]