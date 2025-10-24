# app/api/routes.py
from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import RouteRequest
from app.services.route_service import optimize_route
import requests

router = APIRouter()

@router.post("/optimize")
def optimize(req: RouteRequest):
    """
    Calcula ruta óptima entre origen y destino (lat/lon).
    """
    try:
        return optimize_route(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/geocode")
def geocode(q: str = Query(..., min_length=3)):
    """
    Convierte una dirección a {lat, lon} usando Nominatim (OSM) — demo.
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "LuxChile-MVP/1.0"}
    params = {"q": q, "format": "json", "limit": 1, "addressdetails": 0}
    r = requests.get(url, params=params, headers=headers, timeout=10)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Geocoder externo no disponible")
    data = r.json()
    if not data:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}
