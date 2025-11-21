# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers principales
from app.api.stock import router as stock_router
from app.api.routes import router as routes_router
from app.api.incidents import router as incidents_router
from app.api import asignaciones as asignaciones_router
from app.api.auth import router as auth_router

# Base de datos
from app.db.database import engine, Base, SessionLocal
from app.models import asignaciones as _models_asign
from app.models import users as _models_users
from app.core.security import ensure_default_users

# Crear la app
app = FastAPI(
    title="API Inventario & Rutas - LuxChile",
    version="0.1.0",
    description="API central para gestionar stock, rutas, incidentes y asignaciones de cargas."
)

# CORS para conexión con frontend local y Docker
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://172.20.0.3:5173",  # Red interna de Docker
        "*"  # Permitir todos los orígenes en desarrollo
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

# Crear usuarios por defecto si no existen
try:
    db = SessionLocal()
    ensure_default_users(db)
finally:
    try:
        db.close()
    except Exception:
        pass

# Incluir routers
app.include_router(stock_router, prefix="/stock", tags=["stock"])
app.include_router(routes_router, prefix="/routes", tags=["routes"])
app.include_router(incidents_router, prefix="/incidentes", tags=["incidentes"])
app.include_router(asignaciones_router.router, prefix="/asignaciones", tags=["asignaciones"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


# Endpoint raíz
@app.get("/")
def root():
    return {"ok": True, "service": "LuxChile API", "version": "0.1.0"}
