# Stage 1: Build
FROM node:20-alpine as builder
WORKDIR /app
COPY package.json tsconfig.json tsconfig.node.json vite.config.ts ./
COPY ./src ./src
COPY ./index.html ./
RUN npm install --frozen-lockfile || npm install
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine
WORKDIR /usr/share/nginx/html
COPY --from=builder /app/dist .
COPY --from=builder /app/index.html ./index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
