from pydantic import BaseModel, Field


class UserUpdate(BaseModel):
    num_documento: int = Field(...)
    id_rol: int = Field(...,ge=0)