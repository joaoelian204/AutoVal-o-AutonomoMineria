# Frontend - Vue.js con Nginx
FROM node:20-alpine AS build

WORKDIR /app

# Copiar package.json primero para aprovechar cache
COPY package*.json ./
RUN npm install

# Copiar el resto del código
COPY . .

# Build de producción
RUN npm run build

# Etapa de producción con Nginx
FROM nginx:alpine

# Copiar configuración de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar archivos de build
COPY --from=build /app/dist /usr/share/nginx/html

# Puerto
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
