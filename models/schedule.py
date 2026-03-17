from sqlalchemy import Column, Integer, Time, BigInteger, Date, String, ForeignKey
# 'relationship' DEBE importarse desde .orm
from sqlalchemy.orm import relationship
from db.session import BaseOperative, BaseAdmin

###### CLASES DE LA DB ADMINISTRATIVA (Solo lectura/Validación)
class Persona(BaseAdmin):
    __tablename__ = "persona"
    num_documento = Column(BigInteger, primary_key=True)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)

class Doctor(BaseAdmin):
    __tablename__ = "medicos"

    id_medico = Column(BigInteger, ForeignKey("persona.num_documento"), primary_key=True)
    num_licencia = Column(Integer, unique=True, nullable=False)
    id_especialidad = Column(Integer, nullable=False)

    persona = relationship("Persona", lazy="joined")

###### CLASE DE LA DB OPERATIVA
class Agenda(BaseOperative):
    __tablename__ = "agenda"

    id_agenda = Column(Integer, primary_key=True, index=True)

    # Referencias lógicas (IDs que vienen de la DB Admin)
    id_doctor = Column(BigInteger, nullable=False, index=True)
    id_especialidad = Column(Integer, nullable=False)

    # Definición del bloque
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    # Estado: 1=Activo, 0=Cancelado/Inactivo
    estado = Column(Integer, default=1)