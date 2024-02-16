from fastapi import APIRouter, HTTPException
from ..models import Chalecos, ChalecosIn
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException
import pandas as pd

router = APIRouter()
chalecos_collection = db.chalecos
idic_collection = db.idic



def add_dup_status(x):
    if x == 0:
        return "O"
    else:
        return "D"+str(x)
    
    

@router.post("/chalecos/", response_model=ChalecosIn)
async def crear_chaleco(chaleco: ChalecosIn):
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

    return ChalecosIn(**nuevo_elemento)



# @router.get("/chalecos/", response_model=List[Chalecos])
# async def leer_chalecos():
#     devoluciones = list(chalecos_collection.find())
#     return [Chalecos(**dev) for dev in devoluciones]


@router.get("/chalecos/")
async def leer_chalecos():
    chalecos = list(chalecos_collection.find())
    # Convierte _id de ObjectId a str para cada documento
    chalecos_convertidas = [{**dev, '_id': str(dev['_id'])} if '_id' in dev else dev for dev in chalecos]
    df_chalecos = pd.DataFrame(chalecos_convertidas)
    
    df_chalecos['dup_status'] = df_chalecos.groupby('id_idic').cumcount()
    df_chalecos['dup_status'] = df_chalecos["dup_status"].apply(add_dup_status, 1)
    
    respuesta_final = df_chalecos.to_dict(orient='records')
    return respuesta_final



@router.get("/chalecos/{chaleco_id}", response_model=Chalecos)
async def leer_chaleco(chaleco_id: str):
    chaleco = chalecos_collection.find_one({"_id": ObjectId(chaleco_id)})
    if chaleco:
        return Chalecos(**chaleco)
    raise HTTPException(status_code=404, detail="Chaleco no encontrado")



@router.put("/chalecos/{chaleco_id}", response_model=ChalecosIn)
async def actualizar_chaleco(chaleco_id: str, chaleco_actualizado: ChalecosIn):
    resultado = chalecos_collection.find_one_and_update(
        {"_id": ObjectId(chaleco_id)},
        {"$set": chaleco_actualizado.dict()},
        return_document=True
    )
    if resultado:
        return ChalecosIn(**resultado)
    raise HTTPException(status_code=404, detail="Chaleco no encontrado")



@router.delete("/chalecos/{chaleco_id}", response_model=ChalecosIn)
async def eliminar_chaleco(chaleco_id: str):
    resultado = chalecos_collection.find_one_and_delete({"_id": ObjectId(chaleco_id)})
    if resultado:
        return ChalecosIn(**resultado)
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


