from pydantic import BaseModel, ConfigDict
from datetime import time
from typing import Optional

class ScheduleBase(BaseModel):
    id_medico : int
    dia_semana : str
    hora_inicio : time
    hora_fin : time
    duracion_slot_minutos : int

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id_horario: int

    model_config = ConfigDict(from_attributes=True)

class TimeSlot(BaseModel):
    hora_inicio: time
    hora_fin: time
    disponible: bool = True