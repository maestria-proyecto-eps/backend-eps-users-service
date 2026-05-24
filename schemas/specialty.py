from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class SpecialtyBase(BaseModel):
    nombre_especialidad: str
    descripcion: Optional[str] = None

class SpecialtyResponse(SpecialtyBase):
    id_especialidad: int

    model_config = ConfigDict(from_attributes=True)

# Esquema para la tabla de asociación ESPECIALIDADES_REMITEN
class SpecialtyRemissionResponse(BaseModel):
    id_especialidad_remitida: int
    nombre_remitida: str
    id_especialidad_que_remite: int
    nombre_que_remite: str

    model_config = ConfigDict(from_attributes=True)