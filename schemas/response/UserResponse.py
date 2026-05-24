from pydantic import BaseModel, Field
from typing import Optional
from schemas.response.PersonaResponse import PersonaResponse

class UserResponse(BaseModel):
    id: int = Field(alias="id_usuario")
    num_documento: Optional[int] = None
    id_rol: int
    estado: bool
    rol_des: str
    persona: Optional[PersonaResponse] = None

    model_config={
        "from_attributes": True,
        "populate_by_name": True
    }