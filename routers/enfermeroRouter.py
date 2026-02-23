from fastapi import APIRouter, Depends, status
from dependencies import getEnfermeroService
from schemas.request.EnfermeroCreate import EnfermeroCreate
from schemas.request.EnfermeroUpdate import EnfermeroUpdate
from services.EnfermeroService import EnfermeroService

router = APIRouter(
    prefix="/nurses",
    tags=["Enfermeros"]
)

@router.post("/")
def crear_enfermero(
    data: EnfermeroCreate,
    service: EnfermeroService = Depends(getEnfermeroService)
):
    result = service.add(data)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_201_CREATED)

@router.get("/")
def listar_enfermeros(
    service: EnfermeroService = Depends(getEnfermeroService)
):
    result = service.get_all()
    return result.toHttpResponse(status.HTTP_200_OK)

@router.put("/{id}")
def actualizar_enfermero(
    id: int,
    data: EnfermeroUpdate,
    service: EnfermeroService = Depends(getEnfermeroService)
):
    result = service.update(id, data)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)