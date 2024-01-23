FROM node:21-slim


WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

EXPOSE 3000

RUN chown -R node:node /app
RUN npm update

CMD ["npm", "run", "dev"]