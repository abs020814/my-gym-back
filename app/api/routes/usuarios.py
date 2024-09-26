from logging import info
import logging
from fastapi import APIRouter, Depends, HTTPException
from ...database import get_db
import aiomysql

router = APIRouter()

@router.get("/email", response_model=str)
async def get_por_email(email: str, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        logging.info("en usuarios (entrenadores)")

        await cursor.execute("SELECT emailEntr FROM entrenadores WHERE emailEntr = %s", email)
        resultEntr = await cursor.fetchone()

        if resultEntr is None:
            
            logging.info("en usuarios (clientes)")
            await cursor.execute("SELECT emailClie FROM clientes WHERE emailClie = %s", email)
            resultClie = await cursor.fetchone()
 
            if resultClie is None:

                return "noRegistrado"
            
            else:
            
                return "esCliente"
            
        else:

            return "esEntrenador"


            
