from fastapi import APIRouter, HTTPException
from ..models import Idic
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException



router = APIRouter()
idic_collection = db.idic


@router.post("/idic/", response_model=Idic)
async def crear_idic(idic: Idic):
    resultado = idic_collection.insert_one(idic.dict())
    nuevo_elemento = idic_collection.find_one({"_id": resultado.inserted_id})
    return Idic(**nuevo_elemento)



@router.get("/idic/", response_model=List[Idic])
async def leer_idics():
    idics = list(idic_collection.find())
    return [Idic(**idic) for idic in idics]



@router.get("/idic/{idic_id}", response_model=Idic)
async def leer_idic(idic_id: str):
    idic = idic_collection.find_one({"_id": ObjectId(idic_id)})
    if idic:
        return Idic(**idic)
    raise HTTPException(status_code=404, detail="Idic no encontrado")



@router.put("/idic/{idic_id}", response_model=Idic)
async def actualizar_idic(idic_id: str, idic_actualizado: Idic):
    resultado = idic_collection.find_one_and_update(
        {"_id": ObjectId(idic_id)},
        {"$set": idic_actualizado.dict()},
        return_document=True
    )
    if resultado:
        return Idic(**resultado)
    raise HTTPException(status_code=404, detail="Idic no encontrada")



@router.delete("/idic/{idic_id}", response_model=Idic)
async def eliminar_venta(idic_id: str):
    resultado = idic_collection.find_one_and_delete({"_id": ObjectId(idic_id)})
    if resultado:
        return Idic(**resultado)
    raise HTTPException(status_code=404, detail="Idic no encontrada")
