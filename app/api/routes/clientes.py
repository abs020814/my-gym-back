from fastapi import APIRouter, Depends, HTTPException
from ..models.cliente import Cliente, ClienteBase
from ...database import get_db
import aiomysql
from typing import List

router = APIRouter()

def row_to_cliente(row):
    (idClie,emailClie,nombreClie,objetivosClie,fecAltaClie,fecObjetivoClie,pesoClie,idEntrClie,idRutiClie, idNutrClie) = row

    return Cliente(**{
        "idClie": idClie,
        "emailClie": emailClie,
        "nombreClie": nombreClie,
        "objetivosClie": objetivosClie,
        "fecAltaClie": fecAltaClie,
        "fecObjetivoClie": fecObjetivoClie,
        "pesoClie": pesoClie,
        "idEntrClie": idEntrClie,
        "idRutiClie": idRutiClie,
        "idNutrClie": idNutrClie
    })

@router.get("/all", response_model=List[Cliente])
async def get_clientes_todos(db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT idClie,emailClie,nombreClie,objetivosClie,fecAltaClie,fecObjetivoClie,pesoClie,idEntrClie,idRutiClie, idNutrClie FROM clientes ")
        data = await cursor.fetchall()

        response = []
        for row in data:
            response.append(row_to_cliente(row))
        return response
    
@router.get("/idEntrClie/", response_model=List[Cliente])
async def get_clientes(idEntrClie: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:

        await cursor.execute("SELECT idClie,emailClie,nombreClie,objetivosClie,fecAltaClie,fecObjetivoClie,pesoClie,idEntrClie,idRutiClie,idNutrClie FROM clientes WHERE idEntrClie = %s", (idEntrClie,))
        data = await cursor.fetchall()
        print("geting por idEntrClie: ",data)
        result = [row_to_cliente(row) for row in data] 
        return result
    
@router.get("/idClie/", response_model=Cliente)
async def get_clientes(idClie: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:

        await cursor.execute("SELECT idClie,emailClie,nombreClie,objetivosClie,fecAltaClie,fecObjetivoClie,pesoClie,idEntrClie,idRutiClie,idNutrClie FROM clientes WHERE idClie = %s", (idClie,))
        data = await cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail="Cliente not found")
        print("geting por idClie: ",data)
        return  row_to_cliente(data)

    
@router.get("/emailClie", response_model=Cliente)
async def get_entr_por_email(emailClie: str, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT idClie,emailClie,nombreClie,objetivosClie,fecAltaCLie,fecObjetivoClie,pesoClie,idEntrClie,idRutiClie,idNutrClie FROM clientes WHERE emailClie = %s", (emailClie,))
        result = await cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Cliente not found")
        return row_to_cliente(result)
    
@router.post("/", response_model=List[Cliente])
async def create_cliente( cliente: ClienteBase, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        try:
            await cursor.execute("INSERT INTO clientes (nombreClie,emailClie,objetivosClie,fecObjetivoClie,pesoClie,idEntrClie) VALUES (%s,%s,%s,%s,%s,%s)",
                                (cliente.nombreClie, cliente.emailClie, cliente.objetivosClie, cliente.fecObjetivoClie, cliente.pesoClie,cliente.idEntrClie))
            await db.commit()

            # Verifica cuántas filas fueron afectadas
            if cursor.rowcount == 0:
                raise HTTPException(status_code=400, detail="No se pudo insertar el registro")
        except Exception as e:
            # Manejo de errores
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))      
        
        await cursor.execute("SELECT idClie,emailClie,nombreClie,objetivosClie,fecAltaClie,fecObjetivoClie,pesoClie,idEntrClie,idRutiClie, idNutrClie FROM clientes")

        data = await cursor.fetchall()
        print(data)
        response = []
        for row in data:
            response.append(row_to_cliente(row))
        # print("terminando. . . . . ")
        return response 

        
@router.post("/conEntr", response_model=Cliente)
async def create_cliente_con_entr(cliente: ClienteBase, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        try:    
            await cursor.execute("INSERT INTO clientes (nombreClie,emailClie,objetivosClie,fecObjetivoClie,pesoClie,idEntrClie) VALUES (%s,%s,%s,%s,%s,%s)",
                             (cliente.nombreClie, cliente.emailClie,cliente.objetivosClie,cliente.fecObjetivoClie,cliente.pesoClie,cliente.idEntrClie))
            await db.commit()

            # Verifica cuántas filas fueron afectadas
            if cursor.rowcount == 0:
                raise HTTPException(status_code=400, detail="No se pudo insertar el registro")
        except Exception as e:
            # Manejo de errores
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))      
        
        await cursor.execute("SELECT idClie,emailClie,nombreClie,objetivosClie,fecAltaClie,fecObjetivoClie,pesoClie,idEntrClie,idRutiClie, idNutrClie FROM clientes WHERE idClie = LAST_INSERT_ID()")
        result = await cursor.fetchone()
        return row_to_cliente(result)
        
@router.put("/conEntr", response_model=Cliente)
async def update_cliente(cliente: Cliente, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        print(cliente)
        try:    
            await cursor.execute("UPDATE clientes SET nombreClie=%s,emailClie=%s,objetivosClie=%s,fecObjetivoClie=%s,pesoClie=%s,idEntrClie=%s WHERE idClie = %s",
                             (cliente.nombreClie, cliente.emailClie,cliente.objetivosClie,cliente.fecObjetivoClie,cliente.pesoClie,cliente.idEntrClie,cliente.idClie))
            await db.commit()

        except Exception as e:
            # Manejo de errores
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))      
        
        await cursor.execute("SELECT idClie,emailClie,nombreClie,objetivosClie,fecAltaClie,fecObjetivoClie,pesoClie,idEntrClie,idRutiClie, idNutrClie FROM clientes WHERE idClie = %s",cliente.idClie)
        result = await cursor.fetchone()
        return row_to_cliente(result) 

    
@router.post("/asignEntr", response_model=Cliente)
async def create_cliente(idEntrClie: int, cliente: Cliente, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("INSERT INTO clientes (nombreClie,emailClie,objetivosClie,fecObjetivoClie,pesoClie,idEntrClie) VALUES (%s,%s,%s,%s,%s)",
                             (cliente.nombreClie, cliente.emailClie,cliente.objetivosClie,cliente.fecObjetivoClie,cliente.pesoClie,idEntrClie))
        await db.commit()

        await cursor.execute("SELECT idClie,emailClie,nombreClie,objetivosClie,fecObjetivoClie,pesoClie,idEntrClie,idRutiClie FROM clientes WHERE idEntrClie = %s", (idEntrClie,))
        data = await cursor.fetchall()

        result = [row_to_cliente(row) for row in data] 
        return result

@router.post("/{idClie}/asignRuti", response_model=Cliente)
async def asign_rutina_clie(idClie: int, idRutiClie: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        if idRutiClie == 0 :
            await cursor.execute("UPDATE clientes set idRutiClie = null WHERE idClie = %s", (idClie))
        else :
            await cursor.execute("UPDATE clientes set idRutiClie = %s WHERE idClie = %s", (idRutiClie,idClie))
        
        await db.commit()
        
        await cursor.execute("SELECT idClie,emailClie,nombreClie,objetivosClie,fecAltaClie,fecObjetivoClie,pesoClie,idEntrClie,idRutiClie,idNutrClie FROM clientes WHERE idClie = %s",idClie)
        result = await cursor.fetchone()
        return row_to_cliente(result)

@router.post("/{idClie}/asignNutr", response_model=Cliente)
async def asign_plannutr_clie(idClie: int, idNutrClie: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        if idNutrClie == 0 :
            await cursor.execute("UPDATE clientes set idNutrClie = null WHERE idClie = %s", (idClie))
        else :
            await cursor.execute("UPDATE clientes set idNutrClie = %s WHERE idClie = %s", (idNutrClie,idClie))
        
        await db.commit()
        
        await cursor.execute("SELECT idClie,emailClie,nombreClie,objetivosClie,fecAltaClie,fecObjetivoClie,pesoClie,idEntrClie,idRutiClie,idNutrClie FROM clientes WHERE idClie = %s",idClie)
        result = await cursor.fetchone()
        return row_to_cliente(result)

@router.delete("/{idClie}", response_model=Cliente)
async def delete_comment(idClie: int, db: aiomysql.Connection = Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT idClie,emailClie,nombreClie,objetivosClie,fecAltaClie,fecObjetivoClie,pesoClie,idEntrClie,idRutiClie,idNutrClie FROM clientes WHERE idClie = %s", (idClie,))
        result = await cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Cliente not found")
        
        await cursor.execute("DELETE FROM clientes WHERE idClie = %s", (idClie,))
        await db.commit()

        return (row_to_cliente(result))
    