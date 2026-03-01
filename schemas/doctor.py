from pydantic import BaseModel, ConfigDict
from typing import Optional

class DoctorCreate(BaseModel):

    id_medico: int
    nombres: str
    apellidos: str
    num_licencia: int
    id_especialidad: int
    estado: Optional[int] = 1
    id_usuario: int

class DoctorResponse(BaseModel):
    id_medico: int
    nombres: str
    apellidos: str
    num_licencia: int
    id_especialidad: int
    id_usuario: Optional[int] = None
    estado: int

    model_config = ConfigDict(from_attributes=True)

class DoctorUpdateSpecialty(BaseModel):
    id_especialidad: int