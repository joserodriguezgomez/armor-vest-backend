from pydantic import BaseModel
from typing import Optional
from datetime import date


class Idic(BaseModel):
    id_idic:Optional[int] = None
    lote:str
    serie:str
    talla:str
    idic:str
    poliza_nombre:str
    fecha_poliza:date
    fecha_poliza_vencimiento:date
    

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
    vencimiento_funda:date
    vencimiento_panel:date
    
    
class Ventas(BaseModel):
    id_venta:int
    id_producto:int
    factura:str
    gd:str
    fecha_venta:date
    id_cliente:int
    id_vendedor:int
    comentarios:str
    precio:float
    

class Muestras(BaseModel):
    id_muestra:int
    id_producto:int
    id_cliente:int
    id_vendedor:int
    fecha_muestra:int

    
class Clientes(BaseModel):
    id_cliente:int
    nombre:str
    fecha_creacion:date
    direccion:str
    correo:str
    telefono:str
    comentarios:str
   
    
class Usuarios(BaseModel):
    id_user:int
    user:str
    fecha_creacion:date
    password:str
    rol:str
    



class Devoluciones(BaseModel):
    id_devolucion:int
    id_venta:int
    id_chaleco:int
    fecha_devolucion:date
    motivo:str
    estado:str

