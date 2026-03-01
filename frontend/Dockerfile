FROM node:20-alpine

WORKDIR /app

# Install dependencies first (cached layer)
COPY package*.json .
RUN npm install

# Copy all source files
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
