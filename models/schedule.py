from email.policy import default

from sqlalchemy import Column, Integer, String, Time, ForeignKey
from db.session import Base

class Schedule(Base):
    __tablename__ = "horarios"

    id_horario = Column(Integer, primary_key= True, index=True)
    id_medico = Column(Integer, ForeignKey("medicos.id_medico"))
    dia_semana = Column(String) # Por ejemplo lunes, martes...
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    duracion_slot_minutos = Column(Integer, default=20)
