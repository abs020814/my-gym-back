from datetime import date, datetime, timezone
from typing import List, Optional
from pydantic import BaseModel

class EntrenadorBase(BaseModel):
    nombreEntr: str
    datosEntr: str
    especEntr: str
    emailEntr: str    

class   Entrenador(EntrenadorBase):
    idEntr: int
    fechaAltaEntr: datetime = datetime.now(timezone.utc)  # Valor por defecto
    clientesEntr: Optional[List[int]] = None

    
