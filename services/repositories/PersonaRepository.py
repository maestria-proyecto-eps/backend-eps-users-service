from sqlalchemy import func, select
from sqlalchemy.orm import Session
from models.Persona import Persona


class PersonaRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists_by_documento(self, num_documento: int) -> bool:
        stmt = select(Persona.num_documento).where(Persona.num_documento == num_documento)
        return self.db.scalar(stmt) is not None

    def get_all(self, pag: int, cantidad: int):
        stmt = select(Persona)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.execute(count_stmt).scalar_one()
        offset = (pag - 1) * cantidad
        stmt = stmt.offset(offset).limit(cantidad)
        result = self.db.execute(stmt)
        personas = result.scalars().all()
        return personas, total

    def get_by_documento(self, num_documento: int) -> Persona | None:
        stmt = select(Persona).where(Persona.num_documento == num_documento)
        return self.db.scalar(stmt)

    def add(self, persona: Persona):
        self.db.add(persona)