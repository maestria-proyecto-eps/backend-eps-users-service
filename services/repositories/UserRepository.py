from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload
from models.Usuario import Usuario
from models.Persona import Persona

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
    def get_users(self,rol:int, estado: int, num_documento: int, nombres: str, apellidos: str, pag: int, cantidad: int):
        query = select(Usuario).options(joinedload(Usuario.rol),joinedload(Usuario.persona)).join(Usuario.persona)
        if rol is not None:

            query = query.where(Usuario.id_rol == rol)

        if estado is not None:
            query = query.where(Usuario.estado == estado)
        if num_documento is not None:
            query = query.where(Usuario.num_documento == num_documento)
        if nombres is not None:
            query = query.where(Persona.nombres.ilike(f"%{nombres}%"))
        if apellidos is not None:
            query = query.where(Persona.apellidos.ilike(f"%{apellidos}%"))
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