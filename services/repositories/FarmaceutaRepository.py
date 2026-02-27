from sqlalchemy import select
from sqlalchemy.orm import Session
from models.Farmaceuta import Farmaceuta

class FarmaceutaRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists_by_id(self, id_usuario: int) -> bool:
        stmt = select(Farmaceuta.id_farmaceuta).where(Farmaceuta.id_usuario == id_usuario)
        return self.db.scalar(stmt) is not None

    def get_all(self) -> list[Farmaceuta]:
        stmt = select(Farmaceuta)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, id_usuario: int) -> Farmaceuta | None:
        stmt = select(Farmaceuta).where(Farmaceuta.id_usuario == id_usuario)
        return self.db.scalar(stmt)

    def add(self, farmaceuta: Farmaceuta):
        self.db.add(farmaceuta)

    def delete(self, farmaceuta: Farmaceuta):
        self.db.delete(farmaceuta)