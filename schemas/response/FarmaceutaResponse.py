from pydantic import BaseModel, Field

class FarmaceutaResponse(BaseModel):
    id: int = Field(alias="id_farmaceuta")
    nombres: str
    apellidos: str
    estado: int
    id_usuario: int

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }