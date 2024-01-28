from fastapi import APIRouter, HTTPException
from ..models import Clientes
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException
import pandas as pd

router = APIRouter()
clientes_collection = db.clientes



@router.post("/clientes/", response_model=Clientes)
async def crear_cliente(cliente: Clientes):
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

    return Clientes(**nuevo_elemento)



@router.get("/clientes/", response_model=List[Clientes])
async def leer_clientes():
    result = list(clientes_collection.find())
    return [Clientes(**c) for c in result]



@router.get("/clientes/{cliente_id}", response_model=Clientes)
async def leer_cliente(cliente_id: str):
    cliente = clientes_collection.find_one({"_id": ObjectId(cliente_id)})
    if cliente:
        return Clientes(**cliente)
    raise HTTPException(status_code=404, detail="Cliente no encontrado")



@router.put("/clientes/{cliente_id}", response_model=Clientes)
async def actualizar_cliente(cliente_id: str, cliente_actualizado: Clientes):
    resultado = clientes_collection.find_one_and_update(
        {"_id": ObjectId(cliente_id)},
        {"$set": cliente_actualizado.dict()},
        return_document=True
    )
    if resultado:
        return Clientes(**resultado)
    raise HTTPException(status_code=404, detail="Cliente no encontrado")



@router.delete("/clientes/{chaleco_id}", response_model=Clientes)
async def eliminar_cliente(cliente_id: str):
    resultado = clientes_collection.find_one_and_delete({"_id": ObjectId(cliente_id)})
    if resultado:
        return Clientes(**resultado)
    raise HTTPException(status_code=404, detail="Cliente no encontrado")
