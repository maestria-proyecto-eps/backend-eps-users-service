from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import  relationship
from db.session import Base 


class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario= Column(Integer, primary_key=True)
    username= Column(String(50), nullable=False)
    password= Column(String(50), nullable=False)
    id_rol= Column(Integer,ForeignKey("roles.id_rol"), nullable=False)
    estado= Column(SmallInteger, nullable=False)
    rol = relationship("Role", back_populates="usuarios")

    def __repr__(self):
        return f"<Usuario(id_usuario='{self.id_usuario}', username='{self.username}', password='{self.password}', id_rol='{self.id_rol}', estado='{self.estado}')>"
    