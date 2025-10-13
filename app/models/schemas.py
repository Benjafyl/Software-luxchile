from pydantic import BaseModel, Field
from typing import List, Tuple, Optional

# ---------- STOCK ----------
class ConsultaSKU(BaseModel):
    sku: str

# ---------- RUTAS ----------
class Point(BaseModel):
    lat: float
    lon: float

class RouteSegment(BaseModel):
    coords: List[Tuple[float, float]]  # [(lat, lon), ...]

class RouteRequest(BaseModel):
    origin: Point
    destination: Point

class RouteResponse(BaseModel):
    distance_km: float
    toll_cost: float
    risk_score: float
    duration_min: str    # formato H:MM
    path: RouteSegment

# ---------- INCIDENTES ----------
class IncidentCreate(BaseModel):
    cargo_id: str = Field(..., example="CARGA-123")
    vehicle_id: str = Field(..., example="CAMION-88")
    employee_id: str = Field(..., example="RUT-12345678-9")
    type: str = Field(..., example="DESVIO_RUTA")
    description: Optional[str] = None
    location: Point
