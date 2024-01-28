from fastapi import APIRouter, HTTPException
from ..models import Usuarios
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException
import pandas as pd

router = APIRouter()
usuario_collection = db.usuarios



@router.post("/usuarios/", response_model=Usuarios)
async def crear_cliente(usuario: Usuarios):
    # Encuentra el último ID de póliza
    last_id = usuario_collection.find_one(sort=[("id_usuario", -1)])
    last_id = last_id['id_usuario'] if last_id else 0

    # Incrementa el ID de póliza
    new_id = last_id + 1
    # Actualiza el ID en el objeto Idic
    usuario.id_usuario = new_id

    # Inserta el nuevo documento con el ID incrementado
    resultado = usuario_collection.insert_one(usuario.dict())
    nuevo_elemento = usuario_collection.find_one({"_id": resultado.inserted_id})

    return Usuarios(**nuevo_elemento)



@router.get("/usuario/", response_model=List[Usuarios])
async def leer_usuarios():
    result = list(usuario_collection.find())
    return [Usuarios(**c) for c in result]



@router.get("/usuario/{usuario_id}", response_model=Usuarios)
async def leer_usuario(usuario_id: str):
    usuario = usuario_collection.find_one({"_id": ObjectId(usuario_id)})
    if usuario:
        return Usuarios(**usuario)
    raise HTTPException(status_code=404, detail="Usuario no encontrado")



@router.put("/usuario/{usuario_id}", response_model=Usuarios)
async def actualizar_usuario(usuario_id: str, usuario_actualizado: Usuarios):
    resultado = usuario_collection.find_one_and_update(
        {"_id": ObjectId(usuario_id)},
        {"$set": usuario_actualizado.dict()},
        return_document=True
    )
    if resultado:
        return Usuarios(**resultado)
    raise HTTPException(status_code=404, detail="Usuario no encontrado")



@router.delete("/usuario/{usuario_id}", response_model=Usuarios)
async def eliminar_usuario(usuario_id: str):
    resultado = usuario_collection.find_one_and_delete({"_id": ObjectId(usuario_id)})
    if resultado:
        return Usuarios(**resultado)
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
