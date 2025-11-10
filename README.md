# LuxChile - Sistema de Gestion y Logistica Inteligente

LuxChile es una plataforma web con React + FastAPI para gestionar inventario, rutas, incidentes y asignaciones de cargas.

## Modulos
- Stock: consulta de disponibilidad por SKU.
- Rutas: optimizacion y registro de historial; riesgo y duracion.
- Incidentes: registro y listado con ubicacion.
- Asignaciones: crear, listar, editar (admin) y ver asignaciones del trabajador.

## Autenticacion y roles
- Admin: acceso total (stock, rutas, incidentes, asignaciones CRUD, borrar historiales).
- Worker (chofer): rutas, incidentes y asignaciones propias (filtradas por RUT).
- Usuarios demo: `admin/admin123` y `chofer/chofer123`.

## Puesta en marcha
1) Backend
```
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```
2) Frontend
```
cd frontend
npm install
npm run dev
```
3) Script Windows (opcional)
```
./start-dev.ps1
```

## Configuracion rapida
- API base del front: `frontend/.env` -> `VITE_API_BASE=http://127.0.0.1:8000`
- BD por defecto: `inventario.db` (SQLite)

## Notas tecnicas
- RBAC simple HMAC (tipo JWT) en `app/core/security.py` con dependencias de FastAPI (`HTTPBearer`).
- Endpoints protegidos por rol mediante `require_role()`.
- Asignaciones con SQLAlchemy (`app/models/asignaciones.py`).
- Usuarios seed al iniciar app (`ensure_default_users`).
