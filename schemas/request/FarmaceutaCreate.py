from pydantic import BaseModel, Field

class FarmaceutaCreate(BaseModel):
    nombres: str = Field(..., max_length=50)
    apellidos: str = Field(..., max_length=50)
    estado: int = Field(..., ge=0)
    id_usuario: int = Field(..., ge=0)