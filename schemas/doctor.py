from pydantic import BaseModel
from typing import Optional

class DoctorCreate(BaseModel):
    nombres: str
    apellidos: str
    num_licencia: int
    id_especialidad: int
    id_usuario: Optional[int] = None # Requerido por la DB según el diagrama
    estado: Optional[int] = 1

class DoctorResponse(BaseModel):
    id_medico: int
    nombres: str
    apellidos: str
    num_licencia: int
    id_especialidad: int
    id_usuario: Optional[int] = None
    estado: int

    class Config:
        from_attributes = True

class DoctorUpdateSpecialty(BaseModel):
    id_especialidad: int