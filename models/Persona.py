from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from db.session import Base


class Persona(Base):
    __tablename__ = "persona"

    num_documento = Column(BigInteger, primary_key=True)
    nombres       = Column(String(50), nullable=False)
    apellidos     = Column(String(50), nullable=False)

    usuario = relationship("Usuario", back_populates="persona", uselist=False)

    def __repr__(self):
        return f"<Persona(num_documento={self.num_documento}, nombres={self.nombres}, apellidos={self.apellidos})>"