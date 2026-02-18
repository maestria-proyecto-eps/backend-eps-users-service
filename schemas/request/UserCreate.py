from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    id: int = Field(...)
    username: str = Field(...,max_length=50)
    password: str = Field(...,max_length=50)
    id_rol: int = Field(...,ge=0)