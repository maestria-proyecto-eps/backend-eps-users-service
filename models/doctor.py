from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from db.session import Base

class User(Base):
    __tablename__ = "usuarios"
    # Solo definimos lo mínimo necesario para que la FK de médico funcione
    id_usuario = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)

class Doctor(Base):
    __tablename__ = "medicos"

    id_medico = Column(BigInteger, primary_key=True)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    num_licencia = Column(Integer, unique=True, nullable=False)
    estado = Column(SmallInteger, default=1)

    id_usuario = Column(Integer,ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False, unique=True)
    id_especialidad = Column(Integer,ForeignKey("especialidades.id_especialidad"), nullable=False)

    specialty = relationship("Specialty", back_populates="medicos")
    usuario = relationship("User")#, back_populates="medicos")