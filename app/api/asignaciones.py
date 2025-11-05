# app/api/asignaciones.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.models.asignaciones import Asignacion, Responsable
from app.api.schemas_asignaciones import AsignacionIn, AsignacionOut, ResponsableIn

router = APIRouter()

def _parse_fecha_hora(fecha_hora: str | None):
    if not fecha_hora:
        return None
    iso = fecha_hora.replace(" ", "T")
    try:
        return datetime.fromisoformat(iso)
    except ValueError:
        raise HTTPException(400, "fecha_hora inválida (usa YYYY-MM-DDTHH:MM)")

def _get_or_create_responsable(db: Session, data: ResponsableIn | None) -> Responsable:
    if not data or not data.rut:
        raise HTTPException(400, "responsable.rut (o employee_id) es requerido")
    rut = data.rut.strip().upper()

    resp = db.query(Responsable).filter(Responsable.rut == rut).first()
    if resp:
        # actualiza si vienen datos nuevos
        if data.nombre:
            resp.nombre = data.nombre
        if data.email:
            resp.email = data.email
        if data.telefono:
            resp.telefono = data.telefono
        db.flush()
        return resp

    # nombre por defecto "" para evitar NOT NULL si la columna se dejó nullable=False
    resp = Responsable(
        rut=rut,
        nombre=data.nombre or "",
        email=data.email,
        telefono=data.telefono,
    )
    db.add(resp)
    db.flush()
    return resp

@router.post("", response_model=AsignacionOut)
def crear_asignacion_root(payload: AsignacionIn, db: Session = Depends(get_db)):
    # Validaciones mínimas
    missing = [k for k in ("cargo_id", "vehicle_id", "origen", "destino") if not getattr(payload, k)]
    if missing:
        raise HTTPException(422, detail=f"Faltan campos requeridos: {', '.join(missing)}")

    responsable = _get_or_create_responsable(db, payload.responsable)

    asign = Asignacion(
        cargo_id=payload.cargo_id.strip(),
        vehicle_id=payload.vehicle_id.strip(),
        prioridad=payload.prioridad or "MEDIA",
        origen=payload.origen.strip(),
        destino=payload.destino.strip(),
        fecha_hora=_parse_fecha_hora(payload.fecha_hora),
        notas=(payload.notas or None),
        responsable_id=responsable.id,
    )
    db.add(asign)
    db.commit()
    db.refresh(asign)
    return asign

@router.get("", response_model=list[AsignacionOut])
def listar_asignaciones(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    q = db.query(Asignacion).order_by(Asignacion.id.desc()).limit(limit).all()
    return q
