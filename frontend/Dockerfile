FROM node:20-slim
WORKDIR /usr/src/app
COPY package.json package-lock.json* ./
RUN npm install || true
COPY . .
EXPOSE 5173
CMD ["bash", "-lc", "npm install && npm run dev -- --host"]
