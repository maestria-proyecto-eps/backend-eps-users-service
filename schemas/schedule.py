from pydantic import BaseModel, ConfigDict, model_validator
from datetime import time, date
from typing import Optional

class ScheduleBase(BaseModel):
    id_doctor: int
    id_especialidad: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: Optional[int] = 1

class ScheduleCreate(ScheduleBase):
    @model_validator(mode='after')
    def check_hours(self) -> 'ScheduleCreate':
        if self.hora_inicio >= self.hora_fin:
            raise ValueError("La hora de inicio debe ser anterior a la hora de fin")
        return self

class ScheduleResponse(ScheduleBase):
    id_agenda: int

    model_config = ConfigDict(from_attributes=True)

class TimeSlot(BaseModel):
    hora_inicio: time
    hora_fin: time
    disponible: bool = True

class DoctorSchedule(BaseModel):
    id_doctor: int
    fecha: date
    slots: list[ScheduleResponse]

