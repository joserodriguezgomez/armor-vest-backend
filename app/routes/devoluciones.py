from fastapi import APIRouter, HTTPException
from ..models import Devoluciones, DevolucionesIn
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException



router = APIRouter()
devl_collection = db.devoluciones


@router.post("/devoluciones/", response_model=DevolucionesIn)
async def crear_devolucion(devolucion: DevolucionesIn):
    # Encuentra el último ID de póliza
    last_id = devl_collection.find_one(sort=[("id_devolucion", -1)])
    last_id = last_id['id_devolucion'] if last_id else 0

    # Incrementa el ID de póliza
    new_id = last_id + 1
    # Actualiza el ID en el objeto Idic
    devolucion.id_devolucion = new_id

    # Inserta el nuevo documento con el ID incrementado
    resultado = devl_collection.insert_one(devolucion.dict())
    nuevo_elemento = devl_collection.find_one({"_id": resultado.inserted_id})

    return DevolucionesIn(**nuevo_elemento)



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



@router.put("/devoluciones/{devl_id}", response_model=DevolucionesIn)
async def actualizar_devl(devl_id: str, devl_actualizada: DevolucionesIn):
    resultado = devl_collection.find_one_and_update(
        {"_id": ObjectId(devl_id)},
        {"$set": devl_actualizada.dict()},
        return_document=True
    )
    if resultado:
        return DevolucionesIn(**resultado)
    raise HTTPException(status_code=404, detail="devolución no encontrada")



@router.delete("/devoluciones/{devl_id}", response_model=DevolucionesIn)
async def eliminar_devolucion(devl_id: str):
    resultado = devl_collection.find_one_and_delete({"_id": ObjectId(devl_id)})
    if resultado:
        return DevolucionesIn(**resultado)
    raise HTTPException(status_code=404, detail="Devolución no encontrada")