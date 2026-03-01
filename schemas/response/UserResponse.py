from pydantic import BaseModel, Field

class UserResponse(BaseModel):
    id: int = Field(alias="id_usuario")
    num_documento: int
    id_rol: int
    estado: int
    rol_des: str

    model_config={
        "from_attributes": True,
        "populate_by_name": True
    }