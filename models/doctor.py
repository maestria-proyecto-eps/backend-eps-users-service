from sqlalchemy import BigInteger, Column, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import relationship

from db.session import Base


class Doctor(Base):
    __tablename__ = "medicos"

    id_medico = Column(BigInteger, primary_key=True)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    num_licencia = Column(Integer, unique=True, nullable=False)
    estado = Column(SmallInteger, default=1, nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False, unique=True)
    id_especialidad = Column(Integer, ForeignKey("especialidades.id_especialidad"), nullable=False)

    specialty = relationship("Specialty", back_populates="medicos")
    usuario = relationship("Usuario")
