from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Idic(BaseModel):
    id_idic:Optional[int] = None
    lote:str
    serie:str
    talla:str
    idic:str
    poliza_nombre:str
    fecha_poliza:datetime
    fecha_poliza_vencimiento:datetime
    

class NoIdic(BaseModel):
    id_idic:int
    lote:str
    serie:str
    talla:str


class Chalecos(BaseModel):
    id_chaleco:int
    id_idic:int
    modelo:str
    status:str
    vencimiento_funda:datetime
    vencimiento_panel:datetime
    
    
class Ventas(BaseModel):
    id_venta:int
    id_producto:int
    factura:str
    gd:str
    fecha_venta:datetime
    id_cliente:int
    id_vendedor:int
    comentarios:str
    

class Muestras(BaseModel):
    id_muestra:int
    id_producto:int
    id_cliente:int
    id_vendedor:int
    fecha_muestra:int

    
class Clientes(BaseModel):
    id_cliente:int
    nombre:str
    fecha_creacion:datetime
    direccion:str
    correo:str
    telefono:str
    comentarios:str
   
    
class Usuarios(BaseModel):
    user:str
    fecha_creacion:datetime
    password:str
    rol:str
    

class Devoluciones(BaseModel):
    id_devolucion:int
    id_venta:int
    id_chaleco:int
    fecha_devolucion:datetime
    motivo:str
    estado:str

