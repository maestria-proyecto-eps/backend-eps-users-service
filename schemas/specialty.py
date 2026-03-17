from pydantic import BaseModel, ConfigDict
from typing import Optional

class SpecialtyResponse(BaseModel):
    id_especialidad: int
    nombre_especialidad: str
    requiere_remision: bool

    model_config = ConfigDict(from_attributes=True)
