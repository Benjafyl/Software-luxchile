# Docker Setup - LuxChile

## Requisitos Previos
- Docker Desktop instalado
- Docker Compose instalado

## Estructura de Contenedores
- **Backend**: FastAPI en puerto 8000
- **Frontend**: React + Vite en puerto 5173
- **Base de datos**: SQLite con volumen persistente

## Comandos Rápidos

### Iniciar todos los servicios
```powershell
docker-compose up -d
```

### Ver logs
```powershell
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### Detener servicios
```powershell
docker-compose down
```

### Detener y eliminar volúmenes (¡Cuidado! Borra la base de datos)
```powershell
docker-compose down -v
```

### Reconstruir contenedores
```powershell
docker-compose up -d --build
```

### Ver estado de contenedores
```powershell
docker-compose ps
```

## Acceso a la Aplicación
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## Base de Datos
La base de datos SQLite se almacena en un volumen Docker persistente llamado `db-data`.
Los datos permanecen aunque detengas los contenedores.

## Desarrollo
Los archivos locales están montados como volúmenes, por lo que los cambios en el código se reflejan automáticamente:
- Backend: Hot reload habilitado
- Frontend: Hot Module Replacement (HMR) habilitado

## Troubleshooting

### Puerto ocupado
Si los puertos 8000 o 5173 están ocupados, modifica el archivo `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Cambiar puerto externo
```

### Reiniciar un servicio específico
```powershell
docker-compose restart backend
docker-compose restart frontend
```

### Entrar al contenedor
```powershell
# Backend
docker exec -it luxchile-backend /bin/bash

# Frontend
docker exec -it luxchile-frontend /bin/sh
```

### Ver uso de recursos
```powershell
docker stats
```
