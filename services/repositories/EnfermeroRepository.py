from sqlalchemy import select
from sqlalchemy.orm import Session
from models.Enfermero import Enfermero

class EnfermeroRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists_by_id(self, id_usuario: int) -> bool:
        stmt = select(Enfermero.id_enfermero).where(Enfermero.id_usuario == id_usuario)
        return self.db.scalar(stmt) is not None

    def get_all(self) -> list[Enfermero]:
        stmt = select(Enfermero)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, id_usuario: int) -> Enfermero | None:
        stmt = select(Enfermero).where(Enfermero.id_usuario == id_usuario)
        return self.db.scalar(stmt)

    def add(self, enfermero: Enfermero):
        self.db.add(enfermero)

    def delete(self, enfermero: Enfermero):
        self.db.delete(enfermero)