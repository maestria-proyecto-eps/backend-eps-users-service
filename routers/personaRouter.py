from fastapi import APIRouter, Depends, status
from dependencies import getPersonaService
from schemas.request.PersonaCreate import PersonaCreate
from schemas.request.PersonaUpdate import PersonaUpdate
from schemas.response.PersonaResponse import PersonaResponse
from services.PersonaService import PersonaService
from schemas.response.GenericResponse import Response
from schemas.response.GenericPaginatedResponse import PaginatedResponse
from core.dependencias import RequireRole, get_usuario_actual

router = APIRouter(
    prefix="/persons",
    tags=["Personas"]
)


@router.post("/", response_model=Response[PersonaResponse], dependencies=[Depends(RequireRole(["Talento Humano"]))])
def createPersona(
    persona: PersonaCreate,
    service: PersonaService = Depends(getPersonaService)
):
    result = service.AddPersona(persona)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_201_CREATED)


@router.get("/", response_model=Response[PaginatedResponse[PersonaResponse]], dependencies=[Depends(RequireRole(["Talento Humano"]))])
def getPersonas(
    pag: int = 1,
    cantidad: int = 30,
    service: PersonaService = Depends(getPersonaService)
):
    result = service.GetPersonas(pag, cantidad)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)


@router.get("/{num_documento}", response_model=Response[PersonaResponse], dependencies=[Depends(get_usuario_actual)])
def getPersonaByDocumento(
    num_documento: int,
    service: PersonaService = Depends(getPersonaService)
):
    result = service.GetPersonaByDocumento(num_documento)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)


@router.put("/{num_documento}", response_model=Response[PersonaResponse], dependencies=[Depends(RequireRole(["Talento Humano"]))])
def updatePersona(
    num_documento: int,
    persona: PersonaUpdate,
    service: PersonaService = Depends(getPersonaService)
):
    result = service.UpdatePersonaByDocumento(num_documento, persona)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)