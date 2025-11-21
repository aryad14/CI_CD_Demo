########################################
# DEV STAGE — Hot Reload / Live Changes
########################################
FROM node:20-alpine AS dev
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "dev"]


########################################
# BUILD STAGE — Production Build
########################################
FROM node:20-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build


########################################
# PROD STAGE — Serve via Nginx
########################################
FROM nginx:alpine AS prod
WORKDIR /usr/share/nginx/html

COPY --from=build /app/dist ./

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
