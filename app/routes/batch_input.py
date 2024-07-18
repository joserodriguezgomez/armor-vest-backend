from fastapi import APIRouter, HTTPException, File, UploadFile
from ..models import Product, ProductIn
from ..database import db
from bson import ObjectId
import pandas as pd
from io import BytesIO
from datetime import datetime
from .products import update_dup_values

router = APIRouter()
product_collection = db.products

@router.post("/uploadExcelFile/")
async def upload_excel(file: UploadFile = File(...)):
    last_product = product_collection.find_one(sort=[("idChaleco", -1)])
    if last_product is None:
        last_id = 0
    else:
        last_id = last_product["idChaleco"]
        
    DTYPES = {
        "idChaleco": int,
        "lote": str,
        "serie": str,
        "idic": str,
        "polizaNombre": str,
        "vencimientoPoliza": str,
        "vencimientoPanel": str,
        "modelo": str,
        "status": str,
        "talla": str,
        "precio": float,
        "cliente": str,
        "vendedor": str,
        "factura": str,
        "gd": str,
        "fechaVenta": str,
        "comentarios": str,
        "createdAt": str,
        "createdBy": str,
        "updatedAt": str,
        "updatedBy": str,
        "vencimiento_funda": str,
        "precio_funda": float,
        "dup": str
    }
    
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        # Leer el contenido del archivo en un DataFrame
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents),sheet_name="batch_input", dtype=DTYPES)

        # filename = '/Users/joserodriguez/Desktop/carga_masiva_armor_vest.xlsx'  # Ruta absoluta del archivo
        # df = pd.read_excel(filename, sheet_name="batch_input", dtype=DTYPES)
        
        # Convertir las fechas al formato datetime
        date_columns = ["vencimientoPoliza", "vencimientoPanel", "fechaVenta", "createdAt", "updatedAt", "vencimiento_funda"]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')  # 'coerce' convierte errores en NaT (Not a Time)
        
        df = df.fillna(0)
        df = df[df["talla"] != "0"]
        df_json = df.to_dict(orient="records")
        
        # Convertir los datos a formato JSON compatible con MongoDB
        for record in df_json:
            for field in date_columns:
                if isinstance(record[field], datetime):
                    record[field] = record[field].isoformat()
        
        # Insertar los datos en la base de datos
        product_collection.insert_many(df_json)
        
        await update_dup_values()

        return {"result": "Archivo procesado y datos insertados con éxito"}



@router.get("/deletePoliza/{poliza_nombre}")
async def eliminar_idic(poliza_nombre:str):
    products = []
    cursor = product_collection.find({"polizaNombre": poliza_nombre})
    for document in cursor:
        products.append(document["polizaNombre"])
        

    product_collection.delete_many({"polizaNombre": {"$in": products}})
        
    return "Documentos eliminados con éxito"

