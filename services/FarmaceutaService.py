import math
from models.Farmaceuta import Farmaceuta
from schemas.request.FarmaceutaCreate import FarmaceutaCreate
from schemas.request.FarmaceutaUpdate import FarmaceutaUpdate
from schemas.response.GenericResponse import Response
from schemas.response.GenericPaginatedResponse import PaginatedResponse
from schemas.response.FarmaceutaResponse import FarmaceutaResponse
from services.repositories.FarmaceutaRepository import FarmaceutaRepository
from services.repositories.UserRepository import UserRepository

class FarmaceutaService:
    def __init__(self, repo: FarmaceutaRepository, userRepo: UserRepository):
        self.repo = repo
        self.userRepo = userRepo

    def add(self, data: FarmaceutaCreate):
        user=self.userRepo.get_by_id(data.id_usuario)
        if(user == None):
            return Response.error("Usuario no encontrado")
        if self.repo.exists_by_id(user.num_documento):
            return Response.error("Ya existe un farmaceuta con ese documento")
        farmaceuta = Farmaceuta(**data.model_dump())
        farmaceuta.id_farmaceuta=user.num_documento
        self.repo.add(farmaceuta)
        self.repo.db.commit()
        self.repo.db.refresh(farmaceuta)
        return Response.ok(FarmaceutaResponse.model_validate(farmaceuta), "Farmaceuta creado exitosamente")

    def get_all(self, pag: int, cantidad: int):
        farmaceutas, totalElem = self.repo.get_all(pag, cantidad)
        totalPags = math.ceil(totalElem / cantidad)
        return Response.ok(PaginatedResponse[FarmaceutaResponse](
            data=[FarmaceutaResponse.model_validate(f) for f in farmaceutas], 
            page=pag, 
            pages=totalPags
        ), "Listado de farmaceutas")
    
    def update(self, id: int, data: FarmaceutaUpdate):
        if not self.repo.exists_by_id(id):
            return Response.error("Farmaceuta no encontrado")
        farmaceuta = self.repo.get_by_id(id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(farmaceuta, key, value)
        self.repo.db.commit()
        self.repo.db.refresh(farmaceuta)
        return Response.ok(FarmaceutaResponse.model_validate(farmaceuta), "Farmaceuta actualizado exitosamente")