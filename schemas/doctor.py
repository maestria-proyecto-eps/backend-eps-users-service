from pydantic import BaseModel, ConfigDict


class DoctorCreate(BaseModel):
    id_medico: int
    nombres: str
    apellidos: str
    num_licencia: int
    id_especialidad: int
    estado: int = 1
    id_usuario: int


class DoctorResponse(BaseModel):
    id_medico: int
    nombres: str
    apellidos: str
    num_licencia: int
    id_especialidad: int
    id_usuario: int
    estado: int

    model_config = ConfigDict(from_attributes=True)


class DoctorUpdateSpecialty(BaseModel):
    id_especialidad: int
