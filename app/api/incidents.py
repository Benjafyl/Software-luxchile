from fastapi import APIRouter
from app.models.schemas import IncidentCreate
from app.services.incident_service import create_incident

router = APIRouter(prefix="/incidentes", tags=["incidentes"])

@router.post("/registrar")
def registrar_incidente(body: IncidentCreate):
    new_id = create_incident(body)
    return {"id": new_id, "status": "registrado"}