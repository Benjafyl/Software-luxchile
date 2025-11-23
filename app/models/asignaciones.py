# app/models/asignaciones.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Responsable(Base):
    __tablename__ = "responsables"

    id = Column(Integer, primary_key=True, index=True)
    # Hacemos nombre nullable para evitar el IntegrityError si solo viene el RUT
    nombre = Column(String, nullable=True)
    rut = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, nullable=True)
    email = Column(String, nullable=True)

    asignaciones = relationship("Asignacion", back_populates="responsable")


class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(Integer, primary_key=True, index=True)
    cargo_id = Column(String, nullable=False)
    vehicle_id = Column(String, nullable=False)

    prioridad = Column(String, nullable=False)  # ALTA | MEDIA | BAJA
    estado = Column(String, nullable=False, default="ASIGNADA")  # ASIGNADA | EN_CURSO | COMPLETADA | CANCELADA
    origen = Column(String, nullable=False)
    destino = Column(String, nullable=False)

    fecha_hora = Column(DateTime, nullable=True)  # Fecha programada
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)  # Fecha de creación
    fecha_completada = Column(DateTime, nullable=True)  # Fecha de completación
    notas = Column(Text, nullable=True)

    responsable_id = Column(Integer, ForeignKey("responsables.id"), nullable=False)
    responsable = relationship("Responsable", back_populates="asignaciones")
