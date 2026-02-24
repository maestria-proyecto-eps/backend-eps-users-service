from sqlalchemy import select
from sqlalchemy.orm import Session
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
        stmt = select(Usuario).where(Usuario.id_usuario == user_id)
        return self.db.scalar(stmt)
    def add_user(self, user: Usuario):
        self.db.add(user)