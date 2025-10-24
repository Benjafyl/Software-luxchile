# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.api.stock import router as stock_router
from app.api.routes import router as routes_router
from app.api.incidents import router as incidents_router

# 1) Crear la app primero
app = FastAPI(
    title="API Inventario & Rutas - LuxChile",
    version="0.1.0",
)

# 2) Luego agregar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3) Incluir routers
app.include_router(stock_router, prefix="/stock", tags=["stock"])
app.include_router(routes_router, prefix="/routes", tags=["routes"])
app.include_router(incidents_router, prefix="/incidentes", tags=["incidentes"])

# 4) Endpoint raíz opcional
@app.get("/")
def root():
    return {"ok": True, "service": "LuxChile API"}
