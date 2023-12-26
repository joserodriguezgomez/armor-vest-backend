from fastapi import APIRouter, HTTPException
from ..models import Producto
from ..database import db

router = APIRouter()

# Colección de MongoDB
productos_collection = db.productos



@router.get("/")
async def principal():
    return "hola mundo parte 2"




@router.post("/productos/", response_model=Producto)
async def crear_producto(producto: Producto):
    resultado = productos_collection.insert_one(producto.dict())
    nuevo_producto = productos_collection.find_one({"_id": resultado.inserted_id})
    return Producto(**nuevo_producto)

@router.get("/productos/{producto_id}", response_model=Producto)
async def leer_producto(producto_id: str):
    producto = productos_collection.find_one({"_id": producto_id})
    if producto:
        return Producto(**producto)
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Aquí puedes añadir más rutas para actualizar y eliminar productos
