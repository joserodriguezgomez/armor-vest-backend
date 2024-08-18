from fastapi import APIRouter, HTTPException, Depends
from ..models import Client, ClientIn
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException
import pandas as pd
from passlib.context import CryptContext
from ..auth.routes import oauth2_scheme

router = APIRouter()
client_collection = db.clients
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/clients/")
async def read_clients(token: str = Depends(oauth2_scheme)):
    clients = list(client_collection.find())
    clients_converted = [{**el, '_id': str(el['_id'])} if '_id' in el else el for el in clients]

    return clients_converted



@router.post("/clients/", response_model=ClientIn)
async def create_client(client: ClientIn, token: str = Depends(oauth2_scheme)):
    # Insertar el nuevo producto para obtener su _id
    result = client_collection.insert_one(client.model_dump())
    new_element = client_collection.find_one({"_id": result.inserted_id})
    
    return ClientIn(**new_element)


@router.put("/clients/{client_id}", response_model=ClientIn)
async def update_client(client_id: str, updated_user: ClientIn, token: str = Depends(oauth2_scheme)):
    result = client_collection.find_one_and_update(
        {"_id": ObjectId(client_id)},
        {"$set": updated_user.model_dump()},
        return_document=True
    )
    if result:
        return ClientIn(**result)
    raise HTTPException(status_code=404, detail="Cliente no encontrado")



@router.delete("/clients/{client_id}", response_model=ClientIn)
async def delete_client(client_id: str, token: str = Depends(oauth2_scheme)):
    result = client_collection.find_one_and_delete({"_id": ObjectId(client_id)})
    if result:
        return ClientIn(**result)
    raise HTTPException(status_code=404, detail="Cliente no encontrado")