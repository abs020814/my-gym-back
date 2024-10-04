from datetime import date
from pydantic import BaseModel

class RutinaBase(BaseModel):
    descrRuti: str
    idEntrRuti: int
    diaLbrazosRuti: str

class Rutina(RutinaBase):
    idRuti: int
    fechaAltaRuti: date 

    
