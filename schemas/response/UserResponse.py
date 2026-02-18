from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str
    id_rol: int
    estado: int