from fastapi import APIRouter, Depends, status
from dependencies import getFarmaceutaService
from schemas.request.FarmaceutaCreate import FarmaceutaCreate
from schemas.request.FarmaceutaUpdate import FarmaceutaUpdate
from services.FarmaceutaService import FarmaceutaService
from schemas.response.FarmaceutaResponse import FarmaceutaResponse
from schemas.response.GenericResponse import Response
from schemas.response.GenericPaginatedResponse import PaginatedResponse

router = APIRouter(
    prefix="/pharmacists",
    tags=["Farmaceutas"]
)

@router.post("/", response_model=Response[FarmaceutaResponse])
def crear_farmaceuta(
    data: FarmaceutaCreate,
    service: FarmaceutaService = Depends(getFarmaceutaService)
):
    result = service.add(data)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_201_CREATED)

@router.get("/", response_model=Response[PaginatedResponse[FarmaceutaResponse]])
def listar_farmaceutas(
    pag: int = 1,
    cantidad: int = 30,
    service: FarmaceutaService = Depends(getFarmaceutaService)
):
    result = service.get_all(pag, cantidad)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)

@router.put("/{id}", response_model=Response[FarmaceutaResponse])
def actualizar_farmaceuta(
    id: int,
    data: FarmaceutaUpdate,
    service: FarmaceutaService = Depends(getFarmaceutaService)
):
    result = service.update(id, data)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)