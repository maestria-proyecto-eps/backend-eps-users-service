from pydantic import BaseModel, Field


class PersonaCreate(BaseModel):
    num_documento: int = Field(...)
    nombres: str = Field(..., max_length=50)
    apellidos: str = Field(..., max_length=50)