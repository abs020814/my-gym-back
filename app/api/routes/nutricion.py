from logging import info
import logging
from fastapi import APIRouter, Depends, HTTPException
from ..models.nutricion import Nutricion, NutricionBase
from ...database import get_db
import aiomysql
from typing import List

router = APIRouter()

def row_to_nutricion(row):
    (idNutr,descrNutr,fecAltaNutr,idEntrNutr ) = row

    return Nutricion(**{
        "idNutr": idNutr,
        "descrNutr": descrNutr,
        "fecAltaNutr": fecAltaNutr,
        "idEntrNutr": idEntrNutr
    })

@router.get("/all", response_model=List[Nutricion])
async def get_nutricions(db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        logging.info("en nutricions all---")

        await cursor.execute("SELECT idNutr,descrNutr,fecAltaNutr,idEntrNutr FROM nutricion")
        data = await cursor.fetchall()

        response = []
        for row in data:
            response.append(row_to_nutricion(row))
        return response
        #return [row_to_entrenador(row) for row in data] 
    
@router.post("/", response_model=Nutricion)
async def create_post(nutricion: NutricionBase, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("INSERT INTO nutricion (descrNutr,idEntrNutr) VALUES (%s,%s)",
                             (nutricion.descrNutr, nutricion.idEntrNutr))
        await db.commit()
        await cursor.execute("SELECT idNutr,descrNutr,fecAltaNutr,idEntrNutr FROM nutricion WHERE idNutr = LAST_INSERT_ID()")
        result = await cursor.fetchone()
        return row_to_nutricion(result)
        #return [row_to_entrenador(row) for row in data] 
        
@router.get("/idEntrNutr/{idEntrNutr}", response_model=List[Nutricion])
async def get_Nutr_por_idEntr(idEntrNutr: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT idNutr,descrNutr,fecAltaNutr,idEntrNutr FROM nutricion WHERE idEntrNutr = %s", (idEntrNutr,))
        result = await cursor.fetchall()
        if result is None:
            raise HTTPException(status_code=404, detail="Nutricion not found")
        response = []
        for row in result:
            response.append(row_to_nutricion(row))
        return response

@router.get("/idNutr/{idNutr}", response_model=Nutricion)
async def get_Nutr_por_idEntr(idNutr: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT idNutr,descrNutr,fecAltaNutr,idEntrNutr FROM nutricion WHERE idNutr = %s", (idNutr,))
        result = await cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Nutricion not found")
        return row_to_nutricion(result)

    
@router.delete("/{idNutr}", response_model=Nutricion)
async def delete_post(idNutr: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        
        await cursor.execute("SELECT idNutr,descrNutr,fecAltaNutr,idEntrNutr FROM nutricion WHERE idNutr = %s", (idNutr,))
        result = await cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Nutricion not found")
        
        await cursor.execute("DELETE FROM nutricion WHERE idNutr = %s", (idNutr,))
        await db.commit()

        return row_to_nutricion(result)