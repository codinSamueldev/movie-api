
from config.database import Base
from sqlalchemy import Column, Integer, Float, String 



class Movie(Base):

    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    nombre = Column(String)
    año = Column(Integer)
    categoria = Column(String)
    reseñas = Column(Float(10, 3))

