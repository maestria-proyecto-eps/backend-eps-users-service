from models.Enfermero import Enfermero
from schemas.request.EnfermeroCreate import EnfermeroCreate
from schemas.request.EnfermeroUpdate import EnfermeroUpdate
from schemas.response.GenericResponse import Response
from schemas.response.EnfermeroResponse import EnfermeroResponse
from services.repositories.EnfermeroRepository import EnfermeroRepository
from services.repositories.UserRepository import UserRepository

class EnfermeroService:
    def __init__(self, repo: EnfermeroRepository, userRepo: UserRepository):
        self.repo = repo
        self.userRepo = userRepo

    def add(self, data: EnfermeroCreate):
        user=self.userRepo.get_by_id(data.id_usuario)
        if(user == None):
            return Response.error("Usuario no encontrado")
        enfermero = Enfermero(**data.model_dump())
        enfermero.id_enfermero=user.num_documento
        self.repo.add(enfermero)
        self.repo.db.commit()
        self.repo.db.refresh(enfermero)
        return Response.ok(EnfermeroResponse.model_validate(enfermero), "Enfermero creado exitosamente")

    def get_all(self):
        enfermeros = self.repo.get_all()
        data = [EnfermeroResponse.model_validate(e) for e in enfermeros]
        return Response.ok(data, "Listado de enfermeros")

    def update(self, id: int, data: EnfermeroUpdate):
        if not self.repo.exists_by_id(id):
            return Response.error("Enfermero no encontrado")
        enfermero = self.repo.get_by_id(id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(enfermero, key, value)
        self.repo.db.commit()
        self.repo.db.refresh(enfermero)
        return Response.ok(EnfermeroResponse.model_validate(enfermero), "Enfermero actualizado exitosamente")