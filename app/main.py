from fastapi import FastAPI
from app.api.stock import router as stock_router
from app.api.routes import router as routes_router
from app.api.incidents import router as incidents_router

app = FastAPI(title="API Inventario & Rutas – LuxChile")

app.include_router(stock_router)
app.include_router(routes_router)
app.include_router(incidents_router)
