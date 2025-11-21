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
    duration_min: str    # formato H:MM (compat)
    path: RouteSegment
    # Campos adicionales para presentación local
    duration_hms: str | None = None   # formato HH:MM:SS
    toll_cost_clp: int | None = None  # total peajes en CLP

# ---------- INCIDENTES ----------
class IncidentCreate(BaseModel):
    cargo_id: str = Field(..., example="CARGA-123", description="ID de la carga. Se validará que esté asignada.")
    vehicle_id: str = Field(..., example="CAMION-88", description="ID del vehículo")
    employee_id: str = Field(
        ..., 
        example="12345678-9", 
        description="RUT del conductor (sin puntos, con guión). Debe coincidir con el responsable asignado a la carga."
    )
    type: str = Field(..., example="DESVIO_RUTA", description="Tipo de incidente")
    description: Optional[str] = Field(None, description="Descripción del incidente")
    location: Point = Field(..., description="Ubicación GPS del incidente")
