from datetime import date
from pydantic import BaseModel

class NutricionBase(BaseModel):
    descrNutr: str
    idEntrNutr: int

class Nutricion(NutricionBase):
    idNutr: int
    fecAltaNutr: date 

    
