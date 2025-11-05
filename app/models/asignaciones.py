# app/models/asignaciones.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
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
    origen = Column(String, nullable=False)
    destino = Column(String, nullable=False)

    fecha_hora = Column(DateTime, nullable=True)
    notas = Column(Text, nullable=True)

    responsable_id = Column(Integer, ForeignKey("responsables.id"), nullable=False)
    responsable = relationship("Responsable", back_populates="asignaciones")
