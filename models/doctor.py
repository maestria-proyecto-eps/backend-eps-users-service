from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class Doctor(Base):
    __tablename__ = "medicos"

    id_medico = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    num_licencia = Column(Integer, unique=True, nullable=False)
    estado = Column(SmallInteger, default=1)
    id_usuario = Column(Integer, nullable=True)

    id_especialidad = Column(
        Integer,
        ForeignKey("especialidades.id_especialidad"),
        nullable=False
    )

    specialty = relationship("Specialty", back_populates="medicos")
    # user = relationship("User", back_populates="doctor") # Llave foranea proxima a usar cuando se cree Usuarios