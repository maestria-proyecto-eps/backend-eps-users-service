from sqlalchemy import Column, BigInteger, String, SmallInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base

class Enfermero(Base):
    __tablename__ = "enfermeros"

    id_enfermero = Column(Integer, primary_key=True)
    nombres      = Column(String(50), nullable=False)
    apellidos    = Column(String(50), nullable=False)
    estado       = Column(SmallInteger, nullable=False)
    id_usuario   = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    usuario = relationship("Usuario", backref="enfermeros")

    def __repr__(self):
        return f"<Enfermero(id={self.id_enfermero}, nombres={self.nombres})>"