# app/api/schemas_asignaciones.py
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, model_validator

Prioridad = Literal["ALTA", "MEDIA", "BAJA"]

class ResponsableIn(BaseModel):
    rut: str
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None

class ResponsableOut(BaseModel):
    id: int
    rut: str
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None

    model_config = {"from_attributes": True}

class AsignacionIn(BaseModel):
    # Campos “bonitos” que usa nuestro backend
    cargo_id: Optional[str] = None
    vehicle_id: Optional[str] = None
    prioridad: Optional[Prioridad] = "MEDIA"
    origen: Optional[str] = None
    destino: Optional[str] = None
    fecha_hora: Optional[str] = None  # "YYYY-MM-DDTHH:MM" o "YYYY-MM-DD HH:MM"
    notas: Optional[str] = None
    responsable: Optional[ResponsableIn] = None

    # Alias compatibles con el front anterior
    employee_id: Optional[str] = None            # mapea a responsable.rut
    origin_address: Optional[str] = None         # mapea a origen
    destination_address: Optional[str] = None    # mapea a destino

    @model_validator(mode="before")
    def compat_front(cls, v):
        # Si llega employee_id y no llega responsable, armamos uno
        if v.get("employee_id") and not v.get("responsable"):
            v["responsable"] = {"rut": str(v["employee_id"]).strip()}
        # Direcciones legacy
        if v.get("origin_address") and not v.get("origen"):
            v["origen"] = v["origin_address"]
        if v.get("destination_address") and not v.get("destino"):
            v["destino"] = v["destination_address"]
        return v

    @field_validator("cargo_id", "vehicle_id", "origen", "destino", mode="after")
    def must_not_be_empty(cls, v):
        if v is None:
            return v
        if isinstance(v, str) and not v.strip():
            return None
        return v


class AsignacionOut(BaseModel):
    id: int
    cargo_id: str
    vehicle_id: str
    prioridad: Prioridad
    origen: str
    destino: str
    fecha_hora: Optional[datetime] = None
    notas: Optional[str] = None
    responsable: ResponsableOut

    model_config = {"from_attributes": True}
