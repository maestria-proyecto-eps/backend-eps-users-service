from pydantic import BaseModel, Field


class UserUpdateRole(BaseModel):
    id_rol: int = Field(...,ge=0)