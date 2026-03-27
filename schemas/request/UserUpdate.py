from pydantic import BaseModel, Field
from typing import Optional

class UserUpdate(BaseModel):
    id_rol: int = Field(...,ge=0)
    nombres: Optional[str] = Field(None, max_length=50)
    apellidos: Optional[str] = Field(None, max_length=50)