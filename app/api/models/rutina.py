from datetime import date
from typing import Optional
from pydantic import BaseModel

class RutinaBase(BaseModel):
    descrRuti: str
    idEntrRuti: int
    diasBrazosRuti: Optional[str]
    diasTroncoRuti: Optional[str]

class Rutina(RutinaBase):
    idRuti: int
    fechaAltaRuti: date 

    
