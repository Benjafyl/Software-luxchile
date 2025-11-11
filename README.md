# LuxChile - Sistema de Gestion y Logistica Inteligente

LuxChile es una plataforma web (React + FastAPI) para gestionar inventario, rutas, incidentes y asignaciones de cargas.

## Modulos
- Stock: consulta de disponibilidad por SKU.
- Rutas: optimizacion y registro de historial (distancia, duracion, riesgo).
- Incidentes: registro, listado y eliminacion.
- Asignaciones: crear (admin), listar, editar (admin) y ver asignaciones del trabajador.

## Autenticacion y roles
- Admin: acceso total (stock, rutas, incidentes, asignaciones CRUD, borrar historiales).
- Worker (chofer): acceso a rutas, incidentes y solo sus asignaciones (segun RUT).
- Usuarios demo: `admin/admin123` y `chofer/chofer123`.

## Requisitos
- Python 3.11+ y Node 18+
- Windows, macOS o Linux
- (opcional) PowerShell para usar `start-dev.ps1`

## Puesta en marcha

### Opcion 1: Script Windows
```
./start-dev.ps1
```
Levanta backend + frontend y abre el navegador.

### Opcion 2: Manual
1) Backend
```
python -m venv .venv
./.venv/Scripts/Activate.ps1   # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```
2) Frontend
```
cd frontend
npm install
npm run dev
```

3) Inicializar base de datos (semillas de ejemplo)
```
python -m app.db.init_db
```

## Variables de entorno

### Backend
- `DB_PATH` (por defecto `inventario.db`)
- `AUTH_SECRET` (secreto HMAC para firmar tokens)
- `AUTH_TTL` (TTL del token en segundos; por defecto 86400)

### Frontend
- `VITE_API_BASE` (por defecto `http://127.0.0.1:8000`)

Ejemplo `frontend/.env`:
```
VITE_API_BASE=http://127.0.0.1:8000
```

## Endpoints (resumen)

- Auth
  - `POST /auth/login` -> { access_token, user }
  - `GET  /auth/me`
- Stock
  - `POST /stock/consultar` (admin)
- Rutas
  - `POST /routes/optimize`
  - `GET  /routes/geocode?q=...`
  - `GET  /routes/recent?limit=N`
  - `DELETE /routes/recent/{id}` (admin)
- Incidentes
  - `POST /incidentes/registrar`
  - `GET  /incidentes?limit=N`
  - `DELETE /incidentes/{id}` (admin)
- Asignaciones
  - `GET  /asignaciones?limit=N` (admin ve todas; worker ve las suyas)
  - `POST /asignaciones` (admin)
  - `PUT  /asignaciones/{id}` (admin)
  - `DELETE /asignaciones/{id}` (admin)

## Estructura
```
Software-luxchile/
  app/                # Backend FastAPI
    api/              # Routers (stock, routes, incidents, asignaciones, auth)
    core/             # Seguridad / config
    models/           # SQLAlchemy y Pydantic
    db/               # Conexiones y seeds
    main.py           # Creacion de app y routers
  frontend/           # SPA React + Vite
  requirements.txt    # Dependencias backend
  start-dev.ps1       # Script dev en Windows
  README.md
```

## Notas tecnicas
- RBAC HMAC simple (tipo JWT) en `app/core/security.py` (HTTPBearer de FastAPI).
- Permisos por rol via `require_role()` y `get_current_user()`.
- Asignaciones con SQLAlchemy (`app/models/asignaciones.py`).
- Usuarios por defecto al iniciar (`ensure_default_users`).

## Buenas practicas de repo
- No versionar: `.venv/`, `__pycache__/`, `*.pyc`, `frontend/node_modules/`, caches (`frontend/.vite/`), ni la base `inventario.db`.
- Mantener `frontend/package-lock.json` para reproducibilidad del build del front.

## Documentacion
- Técnica: `docs/Documentacion_Tecnica.md`
- Manual de Usuario: `docs/Manual_Usuario.md`
- Repositorio y Entorno: `docs/Repositorio_y_Entorno.md`
