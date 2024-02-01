from pydantic import BaseModel, Field
from typing import Optional, List, Annotated

class Movie(BaseModel):
    #Set up atributtes
    id: Optional[int] = None
    #Validate data with Field() class.
    nombre: str = Field(min_length=3, max_length=90)
    año: int = Field()
    categoria: str
    reseñas: float

    class Config:
        #Seems like the name always should be schema_extra in order to represent an example.
        schema_extra = {
            "example": {
                "nombre": "Pelicula",
                "año": 2012,
                "categoria": "Tragico/Suspenso",
                "reseñas": 6.6
            }
        }

