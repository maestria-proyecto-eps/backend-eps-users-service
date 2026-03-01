from pydantic import BaseModel, Field
from typing import Optional

class FarmaceutaUpdate(BaseModel):
    nombres: Optional[str] = Field(None, max_length=50)
    apellidos: Optional[str] = Field(None, max_length=50)
    estado: Optional[int] = Field(None, ge=0)