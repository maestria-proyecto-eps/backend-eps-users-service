from sqlalchemy import func,select
from sqlalchemy.orm import Session
from models.Farmaceuta import Farmaceuta

class FarmaceutaRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists_by_id(self, id: int) -> bool:
        stmt = select(Farmaceuta.id_farmaceuta).where(Farmaceuta.id_farmaceuta == id)
        return self.db.scalar(stmt) is not None

    def get_all(self, pag: int, cantidad: int) -> tuple[list[Farmaceuta], int]:
        stmt = select(Farmaceuta)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.execute(count_stmt).scalar_one()
        offset = (pag - 1) * cantidad
        stmt = stmt.offset(offset).limit(cantidad)
        result = self.db.execute(stmt)
        Farmaceutas = result.scalars().all()
        return Farmaceutas, total

    def get_by_id(self, id: int) -> Farmaceuta | None:
        stmt = select(Farmaceuta).where(Farmaceuta.id_farmaceuta == id)
        return self.db.scalar(stmt)

    def add(self, farmaceuta: Farmaceuta):
        self.db.add(farmaceuta)

    def delete(self, farmaceuta: Farmaceuta):
        self.db.delete(farmaceuta)