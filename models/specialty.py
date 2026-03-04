from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from db.session import Base


class Specialty(Base):
    __tablename__ = "especialidades"

    id_especialidad = Column(Integer, primary_key=True, index=True)
    nombre_especialidad = Column(String(50), nullable=False)
    requiere_remision = Column(Boolean, default=False, nullable=False)

    medicos = relationship("Doctor", back_populates="specialty")
