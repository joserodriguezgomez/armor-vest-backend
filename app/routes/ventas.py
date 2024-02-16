from fastapi import APIRouter, HTTPException
from ..models import Ventas, VentasIn
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException
import pandas as pd
import numpy as np




def add_dup_status(x):
    if x == 0:
        return "O"
    else:
        return "D"+str(x)
    
    
# Función para convertir ObjectId a String
def convert_objectid_to_string(data):
    for document in data:
        document['_id'] = str(document['_id'])
    return data


router = APIRouter()
ventas_collection = db.ventas
chalecos_collection = db.chalecos
idic_collection = db.idic
cliente_collection = db.clientes


@router.post("/ventas/", response_model=VentasIn)
async def crear_venta(venta: VentasIn):
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

    return VentasIn(**nuevo_elemento)



@router.get("/ventas/")
async def leer_todas_las_ventas():
    
    chalecos_data = convert_objectid_to_string(list(chalecos_collection.find()))
    idic_data = convert_objectid_to_string(list(idic_collection.find()))
    ventas_data = convert_objectid_to_string(list(ventas_collection.find()))
    clientes_data = convert_objectid_to_string(list(cliente_collection.find()))
    # Verificar si alguna colección está vacía
    if not ventas_data or not chalecos_data or not idic_data:
        # Puedes decidir retornar una lista vacía o lanzar una excepción
        return []  # o raise HTTPException(status_code=404, detail="No se encontraron datos.")
        
    # Convertir a DataFrames de Pandas
    df_ventas = pd.DataFrame(ventas_data)
    df_chalecos = pd.DataFrame(chalecos_data)
    df_idic = pd.DataFrame(idic_data)
    df_clientes = pd.DataFrame(clientes_data)

    # Verificar si los DataFrames están vacíos antes de proceder
    if df_ventas.empty or df_chalecos.empty or df_idic.empty:
        # Manejar el caso de DataFrames vacíos
        return []  # O cualquier otro manejo adecuado

    df_chalecos = df_chalecos.drop(columns=['_id'])  # Excluir columna '_id'
    df_idic = df_idic.drop(columns=['_id'])         # Excluir columna '_id'
    df_clientes = df_clientes.drop(columns=['_id'])   

    df_combinado = pd.merge(df_ventas, df_chalecos, left_on="id_producto", right_on="id_chaleco")
    df_combinado = pd.merge(df_combinado, df_idic, left_on="id_idic", right_on="id_idic")
    df_combinado = pd.merge(df_combinado, df_clientes, left_on="id_cliente", right_on="id_cliente")
    
    
    df_combinado.replace([np.inf, -np.inf, np.nan], None, inplace=True)
    
    df_combinado['dup_status'] = df_combinado.groupby('id_idic').cumcount()
    df_combinado['dup_status'] = df_combinado["dup_status"].apply(add_dup_status, 1)
    
    
    result = df_combinado.to_dict(orient='records')
 
    return result




# Obtener una venta por ID
@router.get("/ventas/{venta_id}", response_model=Ventas)
async def leer_venta(venta_id: str):
    venta = ventas_collection.find_one({"_id": ObjectId(venta_id)})
    if venta:
        return Ventas(**venta)
    raise HTTPException(status_code=404, detail="Venta no encontrada")



@router.put("/ventas/{venta_id}", response_model=VentasIn)
async def actualizar_venta(venta_id: str, venta_actualizada: VentasIn):
    resultado = ventas_collection.find_one_and_update(
        {"_id": ObjectId(venta_id)},
        {"$set": venta_actualizada.dict()},
        return_document=True
    )
    if resultado:
        return VentasIn(**resultado)
    raise HTTPException(status_code=404, detail="Venta no encontrada")



@router.delete("/ventas/{venta_id}", response_model=VentasIn)
async def eliminar_venta(venta_id: str):
    resultado = ventas_collection.find_one_and_delete({"_id": ObjectId(venta_id)})
    if resultado:
        return VentasIn(**resultado)
    raise HTTPException(status_code=404, detail="Venta no encontrada")


