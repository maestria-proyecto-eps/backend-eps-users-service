from sqlalchemy import func, select
from sqlalchemy.orm import Session
from models.Enfermero import Enfermero

class EnfermeroRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists_by_id(self, id: int) -> bool:
        stmt = select(Enfermero.id_enfermero).where(Enfermero.id_enfermero == id)
        return self.db.scalar(stmt) is not None

    def get_all(self, pag: int, cantidad: int) -> tuple[list[Enfermero], int]:
        stmt = select(Enfermero)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.execute(count_stmt).scalar_one()
        offset = (pag - 1) * cantidad
        stmt = (
            stmt
            .offset(offset)
            .limit(cantidad)
        )
        result = self.db.execute(stmt)
        enfermeros = result.scalars().all()
        return enfermeros, total


    def get_by_id(self, id: int) -> Enfermero | None:
        stmt = select(Enfermero).where(Enfermero.id_enfermero == id)
        return self.db.scalar(stmt)

    def add(self, enfermero: Enfermero):
        self.db.add(enfermero)

    def delete(self, enfermero: Enfermero):
        self.db.delete(enfermero)