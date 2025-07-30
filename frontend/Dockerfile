FROM node:20-slim

WORKDIR /app

# Crear package.json si no existe
COPY package*.json ./
RUN if [ ! -f package.json ]; then \
    echo '{"name":"url-health-checker-frontend","version":"0.1.0","private":true}' > package.json; \
    fi

# Instalar dependencias
RUN npm install \
    react@18.2.0 \
    react-dom@18.2.0 \
    @types/react@18.2.61 \
    @types/react-dom@18.2.19 \
    typescript@4.9.5 \
    @mui/material@5.15.11 \
    @mui/icons-material@5.15.11 \
    @emotion/react@11.11.3 \
    @emotion/styled@11.11.0 \
    axios@1.6.7 \
    react-scripts@5.0.1 \
    @types/node@20.11.24 \
    web-vitals@3.5.2

# Copiar archivos del proyecto
COPY . .

# Asegurarse de que los scripts tengan los permisos correctos
RUN chmod +x node_modules/.bin/react-scripts

EXPOSE 3000

ENV CI=false
ENV WDS_SOCKET_PORT=0

# Iniciar el servidor de desarrollo
CMD ["npm", "start"]