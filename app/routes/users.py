from fastapi import APIRouter, HTTPException, Depends
from ..models import User, UserIn
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException
import pandas as pd
from passlib.context import CryptContext
from ..auth.routes import oauth2_scheme

router = APIRouter()
users_collection = db.users
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/users/")
async def read_users(token: str = Depends(oauth2_scheme)):
    users = list(users_collection.find())
    users_converted = [{**el, '_id': str(el['_id'])} if '_id' in el else el for el in users]

    return users_converted



def get_password_hash(password):
    return pwd_context.hash(password)



@router.post("/users/", response_model=UserIn)
async def create_user(user: UserIn, token: str = Depends(oauth2_scheme)):
    user_dict = user.model_dump()
    user_dict["hashed_password"] = get_password_hash(user_dict["hashed_password"])
    # Insertar el nuevo producto para obtener su _id
    result = users_collection.insert_one(user_dict)
    new_element = users_collection.find_one({"_id": result.inserted_id})
    
    return UserIn(**new_element)


@router.put("/users/{user_id}", response_model=UserIn)
async def update_user(user_id: str, updated_user: UserIn, token: str = Depends(oauth2_scheme)):
    result = users_collection.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": updated_user.model_dump()},
        return_document=True
    )
    if result:
        return UserIn(**result)
    raise HTTPException(status_code=404, detail="Usuario no encontrado")



@router.delete("/users/{user_id}", response_model=UserIn)
async def delete_user(user_id: str, token: str = Depends(oauth2_scheme)):
    result = users_collection.find_one_and_delete({"_id": ObjectId(user_id)})
    if result:
        return UserIn(**result)
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


