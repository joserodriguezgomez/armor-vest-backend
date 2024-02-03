from fastapi import APIRouter, HTTPException
from ..models import Chalecos
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException
import pandas as pd

router = APIRouter()
chalecos_collection = db.chalecos
idic_collection = db.idic


@router.post("/chalecos/", response_model=Chalecos)
async def crear_chaleco(chaleco: Chalecos):
    # Encuentra el último ID de póliza
    last_id = chalecos_collection.find_one(sort=[("id_chaleco", -1)])
    last_id = last_id['id_chaleco'] if last_id else 0

    # Incrementa el ID de póliza
    new_id = last_id + 1
    # Actualiza el ID en el objeto Idic
    chaleco.id_chaleco = new_id

    # Inserta el nuevo documento con el ID incrementado
    resultado = chalecos_collection.insert_one(chaleco.dict())
    nuevo_elemento = chalecos_collection.find_one({"_id": resultado.inserted_id})

    return Chalecos(**nuevo_elemento)



@router.get("/chalecos/", response_model=List[Chalecos])
async def leer_chalecos():
    devoluciones = list(chalecos_collection.find())
    return [Chalecos(**dev) for dev in devoluciones]



@router.get("/chalecos/{chaleco_id}", response_model=Chalecos)
async def leer_chaleco(chaleco_id: str):
    chaleco = chalecos_collection.find_one({"_id": ObjectId(chaleco_id)})
    if chaleco:
        return Chalecos(**chaleco)
    raise HTTPException(status_code=404, detail="Chaleco no encontrado")



@router.put("/chalecos/{chaleco_id}", response_model=Chalecos)
async def actualizar_chaleco(chaleco_id: str, chaleco_actualizado: Chalecos):
    resultado = chalecos_collection.find_one_and_update(
        {"_id": ObjectId(chaleco_id)},
        {"$set": chaleco_actualizado.dict()},
        return_document=True
    )
    if resultado:
        return Chalecos(**resultado)
    raise HTTPException(status_code=404, detail="Chaleco no encontrado")



@router.delete("/chalecos/{chaleco_id}", response_model=Chalecos)
async def eliminar_chaleco(chaleco_id: str):
    resultado = chalecos_collection.find_one_and_delete({"_id": ObjectId(chaleco_id)})
    if resultado:
        return Chalecos(**resultado)
    raise HTTPException(status_code=404, detail="Chaleco no encontrado")




@router.get("/chalecos-con-idic")
async def leer_chalecos_con_idic():
    # Obtener datos de MongoDB
    chalecos_data = list(chalecos_collection.find())
    idic_data = list(idic_collection.find())

    # Convertir a DataFrames de Pandas
    df_chalecos = pd.DataFrame(chalecos_data)
    df_idic = pd.DataFrame(idic_data)

    # Combinar los DataFrames
    df_combinado = pd.merge(df_chalecos, df_idic, left_on="id_idic", right_on="id_poliza")

    # Seleccionar solo las columnas necesarias
    df_final = df_combinado[['id_chaleco', 'id_idic', 'modelo', 'stock', 'talla', 'vencimiento_funda', 'vencimiento_panel']]

    # Convertir a formato JSON/dict para la respuesta
    respuesta_final = df_final.to_dict(orient='records')
    
    return respuesta_final


