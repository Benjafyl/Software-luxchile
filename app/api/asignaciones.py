# app/api/asignaciones.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.models.asignaciones import Asignacion, Responsable
from app.models.users import User
from app.api.schemas_asignaciones import AsignacionIn, AsignacionOut, ResponsableIn, AsignacionUpdate
from app.core.security import require_role, get_current_user, AuthUser

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

    # VALIDACIÓN: Verificar que el RUT exista en la tabla users
    user = db.query(User).filter(User.rut == rut).first()
    if not user:
        raise HTTPException(
            400, 
            f"El RUT {rut} no está registrado en el sistema. "
            f"Debe registrar primero al usuario antes de asignarlo como responsable."
        )
    
    # Verificar que el usuario esté activo
    if not user.is_active:
        raise HTTPException(400, f"El usuario con RUT {rut} está inactivo")

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

    # Crear nuevo responsable usando datos del usuario si no se proporcionan
    resp = Responsable(
        rut=rut,
        nombre=data.nombre or user.full_name or "",
        email=data.email,
        telefono=data.telefono,
    )
    db.add(resp)
    db.flush()
    return resp

@router.post("", response_model=AsignacionOut)
def crear_asignacion_root(
    payload: AsignacionIn,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(require_role("admin")),
):
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
    include_completed: bool = Query(False, description="Incluir asignaciones completadas"),
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user),
):
    q = db.query(Asignacion)
    
    # Filtrar por rol
    if user.role == "worker":
        # unir con Responsable para filtrar por rut del usuario
        q = (
            q.join(Responsable, Responsable.id == Asignacion.responsable_id)
            .filter(Responsable.rut == (user.rut or ""))
        )
    
    # Por defecto, excluir completadas del listado reciente
    if not include_completed:
        q = q.filter(Asignacion.estado != "COMPLETADA")
    
    q = q.order_by(Asignacion.id.desc()).limit(limit).all()
    return q


@router.delete("/{asign_id}")
def eliminar_asignacion(
    asign_id: int,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(require_role("admin")),
):
    asign = db.query(Asignacion).filter(Asignacion.id == asign_id).first()
    if not asign:
        raise HTTPException(404, "Asignación no encontrada")
    db.delete(asign)
    db.commit()
    return {"deleted": True, "id": asign_id}


@router.put("/{asign_id}", response_model=AsignacionOut)
def actualizar_asignacion(
    asign_id: int,
    payload: AsignacionUpdate,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(require_role("admin")),
):
    asign = db.query(Asignacion).filter(Asignacion.id == asign_id).first()
    if not asign:
        raise HTTPException(404, "Asignación no encontrada")

    # Posible actualización de responsable
    if payload.responsable:
        resp = _get_or_create_responsable(db, payload.responsable)
        asign.responsable_id = resp.id

    # Actualización de campos simples si vienen presentes
    if payload.cargo_id is not None and payload.cargo_id.strip():
        asign.cargo_id = payload.cargo_id.strip()
    if payload.vehicle_id is not None and payload.vehicle_id.strip():
        asign.vehicle_id = payload.vehicle_id.strip()
    if payload.prioridad is not None:
        asign.prioridad = payload.prioridad
    if payload.estado is not None:
        asign.estado = payload.estado
    if payload.origen is not None and payload.origen.strip():
        asign.origen = payload.origen.strip()
    if payload.destino is not None and payload.destino.strip():
        asign.destino = payload.destino.strip()
    if payload.fecha_hora is not None:
        asign.fecha_hora = _parse_fecha_hora(payload.fecha_hora)
    if payload.notas is not None:
        asign.notas = payload.notas or None

    db.commit()
    db.refresh(asign)
    return asign


@router.patch("/{asign_id}/completar", response_model=AsignacionOut)
def completar_asignacion(
    asign_id: int,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user),
):
    """Marca una asignación como completada. Cualquier usuario puede completar su propia asignación."""
    asign = db.query(Asignacion).filter(Asignacion.id == asign_id).first()
    if not asign:
        raise HTTPException(404, "Asignación no encontrada")
    
    # Si es worker, verificar que sea su asignación
    if user.role == "worker":
        if asign.responsable.rut != user.rut:
            raise HTTPException(403, "No puedes completar asignaciones de otros usuarios")
    
    # Actualizar estado
    asign.estado = "COMPLETADA"
    asign.fecha_completada = datetime.utcnow()
    
    db.commit()
    db.refresh(asign)
    return asign
