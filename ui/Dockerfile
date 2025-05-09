# Use Node.js Alpine image
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package.json tsconfig.json tsconfig.node.json vite.config.ts ./
COPY ./src ./src
COPY ./index.html ./

# Install dependencies
RUN npm install --frozen-lockfile || npm install

# Expose Vite dev server port
EXPOSE 5173

# Start Vite dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
