from sqlalchemy import select
from sqlalchemy.orm import Session
from models.Rol import Role

class RolRepository:
    def __init__(self, db: Session):
        self.db = db
    def exists_by_id(self, id: int) -> bool:
        stmt = select(Role.id_rol).where(Role.id_rol == id)
        return self.db.scalar(stmt) is not None