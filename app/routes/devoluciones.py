from fastapi import APIRouter, HTTPException
from ..models import Devoluciones
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException



router = APIRouter()
devl_collection = db.devoluciones


@router.post("/devoluciones/", response_model=Devoluciones)
async def crear_devolucion(devolucion: Devoluciones):
    resultado = devl_collection.insert_one(devolucion.dict())
    nuevo_elemento = devl_collection.find_one({"_id": resultado.inserted_id})
    return Devoluciones(**nuevo_elemento)



@router.get("/devoluciones/", response_model=List[Devoluciones])
async def leer_devoluciones():
    devoluciones = list(devl_collection.find())
    return [Devoluciones(**dev) for dev in devoluciones]



@router.get("/devoluciones/{devl_id}", response_model=Devoluciones)
async def leer_devolucion(devl_id: str):
    devolucion = devl_collection.find_one({"_id": ObjectId(devl_id)})
    if devolucion:
        return Devoluciones(**devolucion)
    raise HTTPException(status_code=404, detail="Devolución no encontrada")



@router.put("/devoluciones/{devl_id}", response_model=Devoluciones)
async def actualizar_devl(devl_id: str, devl_actualizada: Devoluciones):
    resultado = devl_collection.find_one_and_update(
        {"_id": ObjectId(devl_id)},
        {"$set": devl_actualizada.dict()},
        return_document=True
    )
    if resultado:
        return Devoluciones(**resultado)
    raise HTTPException(status_code=404, detail="devolución no encontrada")



@router.delete("/devoluciones/{devl_id}", response_model=Devoluciones)
async def eliminar_devolucion(devl_id: str):
    resultado = devl_collection.find_one_and_delete({"_id": ObjectId(devl_id)})
    if resultado:
        return Devoluciones(**resultado)
    raise HTTPException(status_code=404, detail="Devolución no encontrada")