from sqlalchemy import Column, Integer, String
from db.session import Base 


class Role(Base):
    __tablename__ = "roles"
    id_rol= Column(Integer, primary_key=True)
    nombre_rol= Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Rol(id_rol='{self.id_rol}', nombre_rol='{self.nombre_rol}')>"