from email.policy import default

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.base import Base

class Specialty(Base):
    __tablename__ = "especialidades"

    id_especialidad = Column(Integer, primary_key=True, index=True)
    nombre_especialidad = Column(String(50), nullable=False)
    requiere_remision = Column(Boolean, default=False)
    dependencia = Column(String(100), nullable=True)

    medicos = relationship("Doctor", back_populates="specialty")