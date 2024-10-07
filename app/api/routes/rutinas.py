from logging import info
import logging
from fastapi import APIRouter, Depends, HTTPException
from ..models.rutina import Rutina, RutinaBase
from ...database import get_db
import aiomysql
from typing import List

router = APIRouter()

def row_to_rutina(row):
    (idRuti,descrRuti,fechaAltaRuti,idEntrRuti,diasBrazosRuti,diasTroncoRuti ) = row

    return Rutina(**{
        "idRuti": idRuti,
        "descrRuti": descrRuti,
        "fechaAltaRuti": fechaAltaRuti,
        "idEntrRuti": idEntrRuti,
        "diasBrazosRuti": diasBrazosRuti,
        "diasTroncoRuti": diasTroncoRuti
    })

@router.get("/all", response_model=List[Rutina])
async def get_rutinas(db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        logging.info("en rutinas all---")

        await cursor.execute("SELECT idRuti,descrRuti,fechaAltaRuti,idEntrRuti,diasBrazosRuti,diasTroncoRuti FROM rutinas")
        data = await cursor.fetchall()

        response = []
        for row in data:
            response.append(row_to_rutina(row))
        return response
        #return [row_to_entrenador(row) for row in data] 
    
@router.post("/", response_model=Rutina)
async def create_post(rutina: RutinaBase, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        logging.info("rutina a grabar: ",rutina)
        await cursor.execute("INSERT INTO rutinas (descrRuti,idEntrRuti,diasBrazosRuti,diasTroncoRuti) VALUES (%s,%s,%s,%s)",
                             (rutina.descrRuti, rutina.idEntrRuti, rutina.diasBrazosRuti, rutina.diasTroncoRuti))
        await db.commit()
        await cursor.execute("SELECT idRuti,descrRuti,fechaAltaRuti,idEntrRuti,diasBrazosRuti,diasTroncoRuti FROM rutinas WHERE idRuti = LAST_INSERT_ID()")
        result = await cursor.fetchone()
        return row_to_rutina(result)
        #return [row_to_entrenador(row) for row in data] 
        
@router.get("/idEntrRuti/{idEntrRuti}", response_model=List[Rutina])
async def get_ruti_por_idEntr(idEntrRuti: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT idRuti,descrRuti,fechaAltaRuti,idEntrRuti,diasBrazosRuti,diasTroncoRuti FROM rutinas WHERE idEntrRuti = %s", (idEntrRuti,))
        result = await cursor.fetchall()
        if result is None:
            raise HTTPException(status_code=404, detail="Rutina not found")
        response = []
        for row in result:
            response.append(row_to_rutina(row))
        return response

@router.get("/idRuti/{idRuti}", response_model=Rutina)
async def get_ruti_por_idEntr(idRuti: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT idRuti,descrRuti,fechaAltaRuti,idEntrRuti,diasBrazosRuti,diasTroncoRuti FROM rutinas WHERE idRuti = %s", (idRuti,))
        result = await cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Rutina not found")
        return row_to_rutina(result)

    
@router.delete("/{idRuti}", response_model=Rutina)
async def delete_post(idRuti: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        
        await cursor.execute("SELECT idRuti,descrRuti,fechaAltaRuti,idEntrRuti,diasBrazosRuti,diasTroncoRuti FROM rutinas WHERE idRuti = %s", (idRuti,))
        result = await cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Rutina not found")
        
        await cursor.execute("DELETE FROM rutinas WHERE idRuti = %s", (idRuti,))
        await db.commit()

        return row_to_rutina(result)