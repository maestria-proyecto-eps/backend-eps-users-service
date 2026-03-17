from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional, Any

class DoctorCreate(BaseModel):

    id_medico: int
    num_licencia: int
    id_especialidad: int

class DoctorResponse(BaseModel):
    id_medico: int
    num_licencia: int
    id_especialidad: int

    # TABLA PERSONA
    nombres: str
    apellidos: str

    model_config = ConfigDict(from_attributes=True)

    # SECCION APORTADA POR IA
    @model_validator(mode='before')
    @classmethod
    def extract_persona_data(cls, data: Any) -> Any:
        # Si la data viene de SQLAlchemy (tiene el atributo 'persona')
        if hasattr(data, "persona") and data.persona:
            # Seteamos manualmente los campos para que Pydantic los vea
            setattr(data, "nombres", data.persona.nombres)
            setattr(data, "apellidos", data.persona.apellidos)
        return data

class DoctorUpdateSpecialty(BaseModel):
    id_especialidad: int