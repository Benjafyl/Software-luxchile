FROM node:22-alpine

WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto de los archivos
COPY . .

# Exponer el puerto de Vite
EXPOSE 5173

# Comando para desarrollo con host 0.0.0.0 para acceso desde fuera del contenedor
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
