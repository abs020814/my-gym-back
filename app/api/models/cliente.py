from datetime import date, datetime, timezone
from typing import Optional
from pydantic import BaseModel

class ClienteBase(BaseModel):
    nombreClie: str
    objetivosClie: str
    fecAltaClie: datetime = datetime.now(timezone.utc)  # Valor por defecto
    fecObjetivoClie: date
    pesoClie: float
    idEntrClie: Optional[int]
    emailClie: str
    idRutiClie: Optional[int]
    idNutrClie: Optional[int]

class Cliente(ClienteBase):
    idClie: int