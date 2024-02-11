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


class Idic(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    id_idic:Optional[int] = None
    lote:str
    serie:str
    idic:str
    poliza_nombre:str
    fecha_poliza:datetime
    fecha_poliza_vencimiento:datetime
 

class IdicIn(BaseModel):
    id_idic:Optional[int] = None
    lote:str
    serie:str
    idic:str
    poliza_nombre:str
    fecha_poliza:datetime
    fecha_poliza_vencimiento:datetime    

class NoIdic(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    id_idic:int
    lote:str
    serie:str
    talla:str


class Chalecos(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    id_chaleco:int
    id_idic:int
    modelo:str
    status:str
    talla:str
    

class ChalecosIn(BaseModel):
    id_chaleco:int
    id_idic:int
    modelo:str
    status:str
    talla:str
    
    
class Ventas(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    id_venta:int
    id_producto:int
    factura:str
    gd:str
    fecha_venta:datetime
    id_cliente:int
    id_vendedor:int
    comentarios:str
    precio:float


class VentasIn(BaseModel):
    id_venta:int
    id_producto:int
    factura:str
    gd:str
    fecha_venta:datetime
    id_cliente:int
    id_vendedor:int
    comentarios:str
    precio:float
    

class Muestras(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    id_muestra:int
    id_producto:int
    id_cliente:int
    id_vendedor:int
    fecha_muestra:int


class MuestrasIn(BaseModel):
    id_muestra:int
    id_producto:int
    id_cliente:int
    id_vendedor:int
    fecha_muestra:int
    
class Clientes(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    id_cliente:int
    nombre:str
    fecha_creacion:datetime
    direccion:str
    correo:str
    telefono:str
    comentarios:str
    
    
class ClientesIn(BaseModel):
    id_cliente:int
    nombre:str
    fecha_creacion:datetime
    direccion:str
    correo:str
    telefono:str
    comentarios:str
   
    
class Usuarios(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    id_user:int
    user:str
    fecha_creacion:datetime
    password:str
    rol:str
    
class UsuariosIn(BaseModel):
    id_user:int
    user:str
    fecha_creacion:datetime
    password:str
    rol:str


class Devoluciones(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    id_devolucion:int
    id_venta:int
    id_chaleco:int
    fecha_devolucion:datetime
    motivo:str
    estado:str

class DevolucionesIn(BaseModel):
    id_devolucion:int
    id_venta:int
    id_chaleco:int
    fecha_devolucion:datetime
    motivo:str
    estado:str