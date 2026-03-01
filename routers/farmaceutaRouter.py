from fastapi import APIRouter, Depends, status
from dependencies import getFarmaceutaService
from schemas.request.FarmaceutaCreate import FarmaceutaCreate
from schemas.request.FarmaceutaUpdate import FarmaceutaUpdate
from services.FarmaceutaService import FarmaceutaService

router = APIRouter(
    prefix="/pharmacists",
    tags=["Farmaceutas"]
)

@router.post("/")
def crear_farmaceuta(
    data: FarmaceutaCreate,
    service: FarmaceutaService = Depends(getFarmaceutaService)
):
    result = service.add(data)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_201_CREATED)

@router.get("/")
def listar_farmaceutas(
    service: FarmaceutaService = Depends(getFarmaceutaService)
):
    result = service.get_all()
    return result.toHttpResponse(status.HTTP_200_OK)

@router.put("/{id}")
def actualizar_farmaceuta(
    id: int,
    data: FarmaceutaUpdate,
    service: FarmaceutaService = Depends(getFarmaceutaService)
):
    result = service.update(id, data)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)