
from fastapi import APIRouter, HTTPException,File, UploadFile
from ..models import Ventas, VentasIn
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException
import pandas as pd
from io import BytesIO



router = APIRouter()
ventas_collection = db.ventas
chalecos_collection = db.chalecos
idic_collection = db.idic
cliente_collection = db.clientes



@router.post("/uploadfile/")
async def upload_excel(file: UploadFile = File(...)):
    
    last_id = chalecos_collection.find_one(sort=[("id_chaleco", -1)])
    if last_id is None:
        last_id = {"id_chaleco": 0}

    last_id_IDIC = idic_collection.find_one(sort=[("id_idic", -1)])
    if last_id_IDIC is None:
        last_id_IDIC = {"id_idic": 0}
        
    last_id_venta = ventas_collection.find_one(sort=[("id_venta", -1)])
    if last_id_venta is None:
        last_id_venta = {"id_venta": 0}

    # Asegurarse de que el archivo sea un Excel
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        # Leer el contenido del archivo en un DataFrame
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents),sheet_name="chalecos")
        df_clientes = pd.read_excel(BytesIO(contents),sheet_name="cliente")
        df_idic = pd.read_excel(BytesIO(contents),sheet_name="IDIC")
        df_ventas = pd.read_excel(BytesIO(contents),sheet_name="ventas")
        
        
        df_idic["id_idic"] = df_idic["id_idic"] + last_id_IDIC["id_idic"]
        df["id_chaleco"] = range(last_id["id_chaleco"] + 1, len(df) + last_id["id_chaleco"] + 1)
        df_ventas["id_producto"] = range(last_id["id_chaleco"] + 1, len(df) + last_id["id_chaleco"] + 1)
        
        # df_ventas["id_venta"] = range(last_id_venta["id_venta"] + 1, len(df_ventas) + last_id_venta["id_venta"] + 1)
        df["id_idic"] = df["id_idic"] + last_id_IDIC["id_idic"]
        # Convertir el DataFrame a JSON para enviarlo como respuesta
        # Nota: Este es un ejemplo simple; podrías necesitar ajustar esto según tus necesidades
        
        df = df[df["status"]!=0]
        df_idic = df_idic[df_idic["serie"]!=0]
        df_ventas = df_ventas[df_ventas["id_cliente"]!=0]
        
        df_ventas["id_venta"] = range(last_id_venta["id_venta"] + 1, len(df_ventas) + last_id_venta["id_venta"] + 1)
        df_idic = df_idic.drop_duplicates(subset=['serie'])
        
        df_json = df.to_dict(orient="records")
        df_json_IDIC = df_idic.to_dict(orient="records")
        df_ventas_json = df_ventas.to_dict(orient="records")
        df_clientes_json = df_clientes.to_dict(orient="records")
        
        
        chalecos_collection.insert_many(df_json)
        idic_collection.insert_many(df_json_IDIC)
        ventas_collection.insert_many(df_ventas_json)
        
        cliente_collection.drop()
        cliente_collection.insert_many(df_clientes_json)
                
        
        return "cargado con éxito"
    else:
        return {"error": "Archivo no soportado"}


@router.get("/deletePoliza/{poliza_nombre}")
async def eliminar_idic(poliza_nombre: int):
    id_idics = []
    cursor = idic_collection.find({"poliza_nombre": poliza_nombre})
    for document in cursor:
        id_idics.append(document["id_idic"])
        
    id_chalecos = []
    chalecos_cursos = chalecos_collection.find({"id_idic": {"$in": id_idics}})    
    for document in chalecos_cursos:
        id_chalecos.append(document["id_chaleco"])
        
    id_ventas = []
    ventas_cursor = ventas_collection.find({"id_producto": {"$in": id_chalecos}})    
    for document in ventas_cursor:
        id_ventas.append(document["id_venta"])


    idic_collection.delete_many({"id_idic": {"$in": id_idics}})
    chalecos_collection.delete_many({"id_chaleco": {"$in": id_chalecos}})
    ventas_collection.delete_many({"id_venta": {"$in": id_idics}})

        
    return "Documentos eliminados con éxito"
        