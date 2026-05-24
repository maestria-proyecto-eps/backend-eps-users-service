from email.policy import default

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base

class Specialty(Base):
    __tablename__ = "especialidades"

    id_especialidad = Column(Integer, primary_key=True, index=True)
    nombre_especialidad = Column(String(50), nullable=False)
    requiere_remision = Column(Boolean, default=False)

    medicos = relationship("Doctor", back_populates="specialty")

    remisiones = relationship(
        "Specialty",
        secondary="especialidades_remiten",
        primaryjoin="Specialty.id_especialidad == SpecialtyRemission.id_especialidad_que_remite",
        secondaryjoin="Specialty.id_especialidad == SpecialtyRemission.id_especialidad_remitida",
        backref="remitido_por"
    )

class SpecialtyRemission(Base):
    __tablename__ = "especialidades_remiten"

    # Clave primaria compuesta y foránea hacia la misma tabla de especialidades
    id_especialidad_remitida = Column(
        Integer,
        ForeignKey("especialidades.id_especialidad"),
        primary_key=True
    )
    id_especialidad_que_remite = Column(
        Integer,
        ForeignKey("especialidades.id_especialidad"),
        primary_key=True
    )