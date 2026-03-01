from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    num_documento: int = Field(...)
    password: str = Field(...,max_length=50)
    id_rol: int = Field(...,ge=0)