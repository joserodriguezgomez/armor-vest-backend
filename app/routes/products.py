from fastapi import APIRouter, HTTPException, Depends
from ..models import Product, ProductIn
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException
import pandas as pd
from ..auth.routes import oauth2_scheme

router = APIRouter()
products_collection = db.products


@router.post("/products/update-dup-values/")
async def update_dup_values():
    # Obtener todos los chalecos de la colección
    chalecos = list(products_collection.find())
    
    # Agrupar chalecos por serie y polizaNombre
    series_polizas = {}
    for chaleco in chalecos:
        serie = chaleco["serie"]
        poliza = chaleco["polizaNombre"]
        key = (serie, poliza)
        if key not in series_polizas:
            series_polizas[key] = []
        series_polizas[key].append(chaleco)
    
    # Recorrer cada serie y polizaNombre y asignar valores de dup
    for key, chalecos_serie_poliza in series_polizas.items():
        chalecos_serie_poliza.sort(key=lambda x: x['idChaleco'])  # Ordenar por idChaleco ascendente
        for idx, chaleco in enumerate(chalecos_serie_poliza):
            if idx == 0:
                dup_value = "O"
            else:
                dup_value = f"D{idx}"
            products_collection.update_one({"_id": ObjectId(chaleco["_id"])}, {"$set": {"dup": dup_value}})
    
    return {"message": "Valores de dup actualizados correctamente para todos los chalecos."}




@router.post("/products/", response_model=ProductIn)
async def create_product(product: ProductIn, token: str = Depends(oauth2_scheme)):
    last_id = products_collection.find_one(sort=[("idChaleco", -1)])
    last_id = last_id['idChaleco'] if last_id else 0

    # Incrementa el ID de póliza
    new_id = last_id + 1
    # Actualiza el ID en el objeto Idic
    product.idChaleco = new_id

    # Insertar el nuevo producto para obtener su _id
    result = products_collection.insert_one(product.model_dump())
    
    await update_dup_values()
    new_element_id = result.inserted_id

    # # Verifica si hay duplicados basados en "serie" y ordena por idChaleco
    # existing_products = list(products_collection.find({"serie": product.serie}).sort("idChaleco", 1))

    # # # Incluye el nuevo producto en la lista
    # # existing_products.append(products_collection.find_one({"_id": new_element_id}))

    # # Ordena por idChaleco nuevamente
    # existing_products.sort(key=lambda x: x['idChaleco'])

    # # Actualiza el campo "dup" de acuerdo al orden de idChaleco
    # for idx, item in enumerate(existing_products):
    #     if idx == 0:
    #         dup_value = "O"
    #     else:
    #         dup_value = f"D{idx}"
    #     products_collection.update_one({"_id": item["_id"]}, {"$set": {"dup": dup_value}})

    new_element = products_collection.find_one({"_id": new_element_id})
    return ProductIn(**new_element)


@router.get("/products/{lote_name}")
async def read_product(lote_name: str, token: str = Depends(oauth2_scheme)):
    if lote_name == "all":
        # Devuelve todos los chalecos sin filtrar por lote
        chalecos = list(products_collection.find())
    else:
        # Filtra los chalecos por el lote especificado
        chalecos = list(products_collection.find({"lote": lote_name}))

    # Convierte _id de ObjectId a str para cada documento
    chalecos_convertidas = [{**el, '_id': str(el['_id'])} if '_id' in el else el for el in chalecos]

    return chalecos_convertidas




@router.put("/products/{product_id}", response_model=ProductIn)
async def update_product(product_id: str, updated_product: ProductIn,token: str = Depends(oauth2_scheme)):
    result = products_collection.find_one_and_update(
        {"_id": ObjectId(product_id)},
        {"$set": updated_product.model_dump()},
        return_document=True
    )
    if result:
        return ProductIn(**result)
    raise HTTPException(status_code=404, detail="Chaleco no encontrado")


@router.delete("/products/{product_id}", response_model=ProductIn)
async def delete_product(product_id: str, token: str = Depends(oauth2_scheme)):
    result = products_collection.find_one_and_delete({"_id": ObjectId(product_id)})
    if result:
        return ProductIn(**result)
    raise HTTPException(status_code=404, detail="Chaleco no encontrado")


@router.get("/lote_summary/")
async def get_resumen_por_lote():
    pipeline = [
        {
            "$group": {
                "_id": {
                    "lote": "$lote",
                    "vencimientoPoliza": "$vencimientoPoliza"
                },
                "vendidos": {"$sum": {"$cond": [{"$eq": ["$status", "vendido"]}, 1, 0]}},
                "stock": {"$sum": {"$cond": [{"$eq": ["$status", "stock"]}, 1, 0]}}
            }
        },
        {
            "$project": {
                "_id": 0,
                "lote": "$_id.lote",
                "vencimientoPoliza": "$_id.vencimientoPoliza",
                "vendidos": 1,
                "stock": 1
            }
        }
    ]
    
    resultado = list(products_collection.aggregate(pipeline))
    if not resultado:
        raise HTTPException(status_code=404, detail="No se encontraron lotes.")
    
    return resultado

