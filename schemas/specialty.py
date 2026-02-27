from pydantic import BaseModel
from typing import Optional

class SpecialtyResponse(BaseModel):
    id_especialidad: int
    nombre_especialidad: str
    requiere_remision: bool
    dependencia: Optional[str] = None

    class Config:
        orm_mode = True
