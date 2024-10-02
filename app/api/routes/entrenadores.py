from logging import info
import logging
from fastapi import APIRouter, Depends, HTTPException
from ..models.entrenador import Entrenador, EntrenadorBase
from ...database import get_db
import aiomysql
from typing import List

router = APIRouter()

def row_to_entrenador(row):
    (idEntr,emailEntr,nombreEntr,estudiosEntr,tarifasEntr,ubicacionEntr,fechaAltaEntr,especEntr,clientesEntr ) = row

    clientesEntr_list = []
    if clientesEntr:
        for idClie in clientesEntr.split(","):
            clientesEntr_list.append(int(idClie))
    else:
        clientesEntr_list= None

    return Entrenador(**{
        "idEntr": idEntr,
        "emailEntr": emailEntr,
        "nombreEntr": nombreEntr,
        "estudiosEntr": estudiosEntr,
        "tarifasEntr": tarifasEntr,
        "ubicacionEntr": ubicacionEntr,
        "fechaAltaEntr": fechaAltaEntr,
        "especEntr": especEntr,
        "clientesEntr": clientesEntr_list,
    })

@router.get("/", response_model=List[Entrenador])
async def get_entrenadores(db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:

        await cursor.execute("SELECT idEntr,emailEntr,nombreEntr,estudiosEntr,tarifasEntr,ubicacionEntr,fechaAltaEntr,especEntr, clientesEntr FROM vw_entrenadores")
        data = await cursor.fetchall()

        response = []
        for row in data:
            response.append(row_to_entrenador(row))
        return response
        #return [row_to_entrenador(row) for row in data] 
    
@router.post("/", response_model=Entrenador)
async def create_entr(entrenador: EntrenadorBase, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("INSERT INTO entrenadores (nombreEntr,estudiosEntr,tarifasEntr,ubicacionEntr,especEntr, emailEntr) VALUES (%s,%s,%s,%s,%s,%s)",
                             (entrenador.nombreEntr, entrenador.estudiosEntr,entrenador.tarifasEntr,entrenador.ubicacionEntr, entrenador.especEntr, entrenador.emailEntr))
        await db.commit()
        await cursor.execute("SELECT idEntr,emailEntr,nombreEntr,estudiosEntr,tarifasEntr,ubicacionEntr,fechaAltaEntr,especEntr, clientesEntr FROM vw_entrenadores WHERE idEntr = LAST_INSERT_ID()")
        result = await cursor.fetchone()
        return row_to_entrenador(result)
        #return [row_to_entrenador(row) for row in data] 

@router.put("/", response_model=Entrenador)
async def modifi_entr(entrenador: Entrenador, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("UPDATE entrenadores SET nombreEntr=%s,estudiosEntr=%s,tarifasEntr=%s,ubicacionEntr=%s,especEntr=%s WHERE idEntr=%s",
                             (entrenador.nombreEntr, entrenador.estudiosEntr,entrenador.tarifasEntr,entrenador.ubicacionEntr, entrenador.especEntr, entrenador.idEntr))
        await db.commit()
        await cursor.execute("SELECT idEntr,emailEntr,nombreEntr,estudiosEntr,tarifasEntr,ubicacionEntr,fechaAltaEntr,especEntr, clientesEntr FROM vw_entrenadores WHERE idEntr = %s",entrenador.idEntr)
        result = await cursor.fetchone()
        return row_to_entrenador(result)
        #return [row_to_entrenador(row) for row in data] 
        
@router.get("/idEntr/{idEntr}", response_model=Entrenador)
async def get_entr_por_id(idEntr: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT idEntr,emailEntr,nombreEntr,estudiosEntr,tarifasEntr,ubicacionEntr,fechaAltaEntr,especEntr, clientesEntr FROM vw_entrenadores WHERE idEntr = %s", (idEntr,))
        result = await cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Entrenador not found")
        return row_to_entrenador(result)
    
@router.get("/emailEntr", response_model=Entrenador)
async def get_entr_por_email(emailEntr: str, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT idEntr,emailEntr,nombreEntr,estudiosEntr,tarifasEntr,ubicacionEntr,fechaAltaEntr,especEntr, clientesEntr FROM vw_entrenadores WHERE emailEntr = %s", (emailEntr,))
        result = await cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Entrenador not found")
        return row_to_entrenador(result)
    
@router.delete("/{idEntr}", response_model=Entrenador)
async def delete_entr(idEntr: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        info(idEntr)
        await cursor.execute("SELECT idEntr,emailEntr,nombreEntr,estudiosEntr,tarifasEntr,ubicacionEntr,fechaAltaEntr,especEntr, clientesEntr FROM vw_entrenadores WHERE idEntr = %s", (idEntr,))
        result = await cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Entrenador not found")
        
        await cursor.execute("DELETE FROM entrenadores WHERE idEntr = %s", (idEntr,))
        await db.commit()

        return row_to_entrenador(result)