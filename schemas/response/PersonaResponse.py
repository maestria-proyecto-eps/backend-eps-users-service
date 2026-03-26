from pydantic import BaseModel, Field


class PersonaResponse(BaseModel):
    num_documento: int
    nombres: str
    apellidos: str


    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }