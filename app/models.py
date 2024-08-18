from pydantic import BaseModel, Field, validator
from typing import Optional,List, Dict, Any
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError(f'Invalid ObjectId: {v}')
        return str(v)  # Convertimos el ObjectId a string para la serialización



 
class Product(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    idChaleco:Optional[int] = None
    lote:str
    serie:str
    idic:str
    polizaNombre:str
    vencimientoPoliza:datetime
    vencimientoPanel:datetime 
    modelo:str
    status:str
    talla:str
    precio:float
    cliente:str
    vendedor:str
    factura:str
    gd:str
    fechaVenta:datetime
    comentarios:str
    createdAt:datetime
    createdBy:str
    updatedAt:datetime
    updatedBy:str
    vencimiento_funda:datetime
    precio_funda:float
    dup:str
    
 
 
class ProductIn(BaseModel):
    idChaleco:Optional[int] = None
    lote:str
    serie:str
    idic:str
    polizaNombre:str
    vencimientoPoliza:datetime
    vencimientoPanel:datetime 
    modelo:str
    status:str
    talla:str
    precio:float
    cliente:str
    vendedor:str
    factura:str
    gd:str
    fechaVenta:datetime
    comentarios:str
    createdAt:datetime
    createdBy:str
    updatedAt:datetime
    updatedBy:str
    vencimiento_funda:datetime
    precio_funda:float
    dup:str
 


   
    
class User(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    username:str
    email:str
    full_name:str
    hashed_password:str
    disabled:bool
    alias:str
    role: str
    
class UserIn(BaseModel):
    username:str
    email:str
    full_name:str
    hashed_password:str
    disabled:bool
    alias:str
    role: str
    
class Client(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    name:str
    rut:str


class ClientIn(BaseModel):
    name:str
    rut:str