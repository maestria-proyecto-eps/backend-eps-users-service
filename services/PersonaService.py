import math
from models.Persona import Persona
from schemas.request.PersonaCreate import PersonaCreate
from schemas.request.PersonaUpdate import PersonaUpdate
from schemas.response.GenericResponse import Response
from schemas.response.PersonaResponse import PersonaResponse
from schemas.response.GenericPaginatedResponse import PaginatedResponse
from services.repositories.PersonaRepository import PersonaRepository


class PersonaService:
    def __init__(self, repo: PersonaRepository):
        self.repo = repo

    def AddPersona(self, data: PersonaCreate):
        if self.repo.exists_by_documento(data.num_documento):
            return Response.error("Ya existe una persona con ese número de documento")
        persona = Persona(**data.model_dump())
        self.repo.add(persona)
        self.repo.db.commit()
        self.repo.db.refresh(persona)
        return Response.ok(PersonaResponse.model_validate(persona), "Persona creada exitosamente")

    def GetPersonas(self, pag: int, cantidad: int):
        personas, totalElem = self.repo.get_all(pag, cantidad)
        totalPags = math.ceil(totalElem / cantidad)
        return Response.ok(PaginatedResponse[PersonaResponse](
            data=[PersonaResponse.model_validate(p) for p in personas],
            page=pag,
            pages=totalPags
        ), "Listado de personas")

    def GetPersonaByDocumento(self, num_documento: int):
        persona = self.repo.get_by_documento(num_documento)
        if persona is None:
            return Response.error("Persona no encontrada")
        return Response.ok(PersonaResponse.model_validate(persona), "Persona obtenida exitosamente")

    def UpdatePersonaByDocumento(self, num_documento: int, data: PersonaUpdate):
        persona = self.repo.get_by_documento(num_documento)
        if persona is None:
            return Response.error("Persona no encontrada")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(persona, key, value)
        self.repo.db.commit()
        self.repo.db.refresh(persona)
        return Response.ok(PersonaResponse.model_validate(persona), "Persona actualizada exitosamente")