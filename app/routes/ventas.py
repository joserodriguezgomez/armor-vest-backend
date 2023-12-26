from fastapi import APIRouter, HTTPException
from ..models import Ventas
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException



router = APIRouter()
ventas_collection = db.ventas


@router.post("/ventas/", response_model=Ventas)
async def crear_producto(venta: Ventas):
    resultado = ventas_collection.insert_one(venta.dict())
    nuevo_producto = ventas_collection.find_one({"_id": resultado.inserted_id})
    return Ventas(**nuevo_producto)


# Obtener todas las ventas
@router.get("/ventas/", response_model=List[Ventas])
async def leer_todas_las_ventas():
    ventas = list(ventas_collection.find())
    return [Ventas(**venta) for venta in ventas]


# Obtener una venta por ID
@router.get("/ventas/{venta_id}", response_model=Ventas)
async def leer_venta(venta_id: str):
    venta = ventas_collection.find_one({"_id": ObjectId(venta_id)})
    if venta:
        return Ventas(**venta)
    raise HTTPException(status_code=404, detail="Venta no encontrada")



@router.put("/ventas/{venta_id}", response_model=Ventas)
async def actualizar_venta(venta_id: str, venta_actualizada: Ventas):
    resultado = ventas_collection.find_one_and_update(
        {"_id": ObjectId(venta_id)},
        {"$set": venta_actualizada.dict()},
        return_document=True
    )
    if resultado:
        return Ventas(**resultado)
    raise HTTPException(status_code=404, detail="Venta no encontrada")



@router.delete("/ventas/{venta_id}", response_model=Ventas)
async def eliminar_venta(venta_id: str):
    resultado = ventas_collection.find_one_and_delete({"_id": ObjectId(venta_id)})
    if resultado:
        return Ventas(**resultado)
    raise HTTPException(status_code=404, detail="Venta no encontrada")


