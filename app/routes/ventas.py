from fastapi import APIRouter, HTTPException
from ..models import Ventas
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException
import pandas as pd


# Función para convertir ObjectId a String
def convert_objectid_to_string(data):
    for document in data:
        document['_id'] = str(document['_id'])
    return data


router = APIRouter()
ventas_collection = db.ventas
chalecos_collection = db.chalecos
idic_collection = db.idic


@router.post("/ventas/", response_model=Ventas)
async def crear_venta(venta: Ventas):
    # Encuentra el último ID de póliza
    last_id = ventas_collection.find_one(sort=[("id_venta", -1)])
    last_id = last_id['id_venta'] if last_id else 0

    # Incrementa el ID de póliza
    new_id = last_id + 1
    # Actualiza el ID en el objeto Idic
    venta.id_venta = new_id

    # Inserta el nuevo documento con el ID incrementado
    resultado = ventas_collection.insert_one(venta.dict())
    nuevo_elemento = ventas_collection.find_one({"_id": resultado.inserted_id})
    
    print(nuevo_elemento)
    # Actualizar el estado del chaleco correspondiente a "vendido"
    chalecos_collection.update_one(
        {'id_chaleco': nuevo_elemento['id_producto']},
        {'$set': {'status': 'vendido'}}
    )

    return Ventas(**nuevo_elemento)


# Obtener todas las ventas
@router.get("/ventas/")
async def leer_todas_las_ventas():
    
    chalecos_data = convert_objectid_to_string(list(chalecos_collection.find()))
    idic_data = convert_objectid_to_string(list(idic_collection.find()))
    ventas_data = convert_objectid_to_string(list(ventas_collection.find()))
        
    # Convertir a DataFrames de Pandas
    df_ventas = pd.DataFrame(ventas_data)
    df_chalecos = pd.DataFrame(chalecos_data).drop(columns=['_id'])  # Excluir columna '_id'
    df_idic = pd.DataFrame(idic_data).drop(columns=['_id'])         # Excluir columna '_id'
    df_combinado = pd.merge(df_ventas, df_chalecos, left_on="id_producto", right_on="id_chaleco")
    df_combinado = pd.merge(df_combinado, df_idic, left_on="id_idic", right_on="id_idic")
    
    result = df_combinado.to_dict(orient='records')

    return result



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


