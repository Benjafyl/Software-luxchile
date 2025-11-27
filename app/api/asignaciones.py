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

def validar_rut_conductor_en_asignacion(db: Session, cargo_id: str, employee_rut: str) -> tuple[bool, str]:
    """
    Valida que el RUT del empleado corresponda al responsable asignado a la carga.
    
    Args:
        db: Sesión de base de datos
        cargo_id: ID de la carga
        employee_rut: RUT del empleado que registra el incidente
    
    Returns:
        tuple[bool, str]: (es_valido, mensaje_error)
    """
    # Normalizar RUT
    employee_rut = employee_rut.strip().upper()
    
    # Buscar asignación activa para esta carga
    asignacion = (
        db.query(Asignacion)
        .join(Responsable, Responsable.id == Asignacion.responsable_id)
        .filter(Asignacion.cargo_id == cargo_id)
        .order_by(Asignacion.id.desc())
        .first()
    )
    
    if not asignacion:
        return False, f"No existe asignación para la carga {cargo_id}"
    
    if not asignacion.responsable:
        return False, f"La asignación {cargo_id} no tiene responsable asignado"
    
    # Validar que el RUT coincida
    if asignacion.responsable.rut != employee_rut:
        return False, (
            f"RUT no autorizado. El conductor asignado a la carga {cargo_id} es "
            f"{asignacion.responsable.nombre or 'N/A'} (RUT: {asignacion.responsable.rut}). "
            f"RUT ingresado: {employee_rut}"
        )
    
    return True, "RUT validado correctamente"

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
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user),
):
    q = db.query(Asignacion)
    if user.role == "worker":
        # unir con Responsable para filtrar por rut del usuario
        q = (
            q.join(Responsable, Responsable.id == Asignacion.responsable_id)
            .filter(Responsable.rut == (user.rut or ""))
        )
    q = q.order_by(Asignacion.id.desc()).limit(limit).all()
    return q


@router.get("/cargo/{cargo_id}", response_model=AsignacionOut | None)
def obtener_asignacion_por_carga(
    cargo_id: str,
    db: Session = Depends(get_db),
    user: AuthUser = Depends(get_current_user),
):
    """
    Obtiene la asignación más reciente para un cargo_id específico.
    Útil para verificar qué conductor está asignado a una carga.
    """
    asignacion = (
        db.query(Asignacion)
        .filter(Asignacion.cargo_id == cargo_id)
        .order_by(Asignacion.id.desc())
        .first()
    )
    
    if not asignacion:
        raise HTTPException(404, f"No se encontró asignación para la carga {cargo_id}")
    
    # Si es worker, verificar que sea su asignación
    if user.role == "worker":
        if asignacion.responsable.rut != user.rut:
            raise HTTPException(403, "No tienes permiso para ver esta asignación")
    
    return asignacion


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
