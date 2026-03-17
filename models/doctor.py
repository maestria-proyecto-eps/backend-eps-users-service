from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from db.session import Base

# CLASE REALIZADA CON FINALIDAD DE PRUEBAS
class Persona(Base):
    __tablename__ = "persona"
    num_documento = Column(BigInteger, primary_key=True)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)

class Doctor(Base):
    __tablename__ = "medicos"

    id_medico = Column(BigInteger, ForeignKey("persona.num_documento"), primary_key=True)
    num_licencia = Column(Integer, unique=True, nullable=False)
    id_especialidad = Column(Integer,ForeignKey("especialidades.id_especialidad"), nullable=False)

    specialty = relationship("Specialty", back_populates="medicos")
    persona = relationship("Persona", lazy="joined")