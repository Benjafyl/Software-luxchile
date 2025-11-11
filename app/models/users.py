from sqlalchemy import Column, Integer, String
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    rut = Column(String, nullable=True, index=True)  # RUT del trabajador (si aplica)
    role = Column(String, nullable=False)  # 'admin' | 'worker'
    hashed_password = Column(String, nullable=False)
    is_active = Column(Integer, default=1)

