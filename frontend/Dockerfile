FROM node:20.0.0 as admin-build-stage
RUN echo "NODE Version:" && node --version
WORKDIR /app

COPY package*.json ./

RUN npm config set fetch-retry-maxtimeout 120000

RUN npm i --force

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

