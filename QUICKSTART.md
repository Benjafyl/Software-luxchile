# Guía Rápida de Inicio

## 🐳 Inicio con Docker (Más fácil)

1. **Asegúrate de tener Docker Desktop instalado y corriendo**

2. **Inicia todos los servicios:**
   ```powershell
   .\start-docker.ps1
   ```

3. **Accede a la aplicación:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Documentación API: http://localhost:8000/docs

4. **Credenciales de prueba:**
   - Admin: `admin` / `admin123`
   - Chofer: `chofer` / `chofer123`

5. **Para detener:**
   ```powershell
   .\stop-docker.ps1
   ```

## 📋 Comandos Útiles

### Ver logs en tiempo real
```powershell
docker-compose logs -f
```

### Ver logs de un servicio específico
```powershell
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Reiniciar servicios
```powershell
docker-compose restart
```

### Reconstruir después de cambios en dependencias
```powershell
docker-compose up -d --build
```

### Entrar a un contenedor
```powershell
# Backend
docker exec -it luxchile-backend /bin/bash

# Frontend
docker exec -it luxchile-frontend /bin/sh
```

## 🔧 Troubleshooting

### El puerto está ocupado
Edita `docker-compose.yml` y cambia el puerto:
```yaml
ports:
  - "8001:8000"  # Cambiar 8000 por otro puerto
```

### Los cambios no se reflejan
```powershell
docker-compose restart
```

### Limpiar todo y empezar de cero
```powershell
docker-compose down -v
docker-compose up -d --build
```

## 📚 Documentación Completa
Ver [README.Docker.md](README.Docker.md) para más detalles.
