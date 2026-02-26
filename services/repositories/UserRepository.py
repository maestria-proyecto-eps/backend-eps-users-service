from typing import List

from sqlalchemy import Tuple, func, select
from sqlalchemy.orm import Session, joinedload
from models import Rol
from models.Usuario import Usuario

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    def exists_by_id(self, id: int) -> bool:
        stmt = select(Usuario.id_usuario).where(Usuario.id_usuario == id)
        return self.db.scalar(stmt) is not None
    def exists_by_numId(self, numId: int) -> bool:
        stmt = select(Usuario.id_usuario).where(Usuario.num_documento == numId)
        return self.db.scalar(stmt) is not None
    def get_by_id(self, user_id: int) -> Usuario | None:
        stmt = select(Usuario).options(joinedload(Usuario.rol)).where(Usuario.id_usuario == user_id)
        return self.db.scalar(stmt)
    def add_user(self, user: Usuario):
        self.db.add(user)
    def get_users(self,rol:int, estado: int, pag: int, cantidad: int) -> Tuple[List["Usuario"], int]:
        query = select(Usuario).options(joinedload(Usuario.rol))
        if rol is not None:

            query = query.where(Usuario.id_rol == rol)

        if estado is not None:
            query = query.where(Usuario.estado == estado)

        count_query = select(func.count()).select_from(query.subquery())
        total = self.db.execute(count_query).scalar_one()
        offset = (pag - 1) * cantidad

        query = (
            query
            .offset(offset)
            .limit(cantidad)
        )

        result = self.db.execute(query)
        usuarios = result.scalars().all()
    
        return usuarios, total