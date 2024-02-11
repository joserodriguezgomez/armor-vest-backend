from fastapi import APIRouter, HTTPException
from ..models import Clientes, ClientesIn
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException
import pandas as pd

router = APIRouter()
clientes_collection = db.clientes



@router.post("/clientes/", response_model=ClientesIn)
async def crear_cliente(cliente: ClientesIn):
    # Encuentra el último ID de póliza
    last_id = clientes_collection.find_one(sort=[("id_cliente", -1)])
    last_id = last_id['id_cliente'] if last_id else 0

    # Incrementa el ID de póliza
    new_id = last_id + 1
    # Actualiza el ID en el objeto Idic
    cliente.id_cliente = new_id

    # Inserta el nuevo documento con el ID incrementado
    resultado = clientes_collection.insert_one(cliente.dict())
    nuevo_elemento = clientes_collection.find_one({"_id": resultado.inserted_id})

    return ClientesIn(**nuevo_elemento)



# @router.get("/clientes/", response_model=List[Clientes])
# async def leer_clientes():
#     result = list(clientes_collection.find())
#     return [Clientes(**c) for c in result]


@router.get("/clientes/", response_model=List[Clientes])
async def leer_clientes():
    result = list(clientes_collection.find())
    # Convierte _id de ObjectId a str para cada documento
    result_convertido = [{**c, '_id': str(c['_id'])} if '_id' in c else c for c in result]
    return [Clientes(**c) for c in result_convertido]




@router.get("/clientes/{cliente_id}", response_model=Clientes)
async def leer_cliente(cliente_id: str):
    cliente = clientes_collection.find_one({"_id": ObjectId(cliente_id)})
    if cliente:
        return Clientes(**cliente)
    raise HTTPException(status_code=404, detail="Cliente no encontrado")



@router.put("/clientes/{cliente_id}", response_model=ClientesIn)
async def actualizar_cliente(cliente_id: str, cliente_actualizado: ClientesIn):
    resultado = clientes_collection.find_one_and_update(
        {"_id": ObjectId(cliente_id)},
        {"$set": cliente_actualizado.dict()},
        return_document=True
    )
    if resultado:
        return ClientesIn(**resultado)
    raise HTTPException(status_code=404, detail="Cliente no encontrado")



@router.delete("/clientes/{cliente_id}", response_model=ClientesIn)
async def eliminar_cliente(cliente_id: str):
    resultado = clientes_collection.find_one_and_delete({"_id": ObjectId(cliente_id)})
    if resultado:
        return ClientesIn(**resultado)
    raise HTTPException(status_code=404, detail="Cliente no encontrado")
