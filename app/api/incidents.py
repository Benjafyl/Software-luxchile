# app/api/incidents.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import IncidentCreate
from app.services.incident_service import registrar_incidente

router = APIRouter()

@router.post("/registrar")
def registrar(data: IncidentCreate):
    try:
        return registrar_incidente(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
