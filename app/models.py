from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Define un modelo Pydantic para tus datos
class Producto(BaseModel):
    id: Optional[str]
    nombre: str
    descripcion: str
    precio: float


class Idic(BaseModel):
    id_poliza:int
    lote:str
    serie:str
    talla:str
    idic:str
    poliza_nombre:str
    fecha_poliza:datetime
    

class Chalecos(BaseModel):
    id_chaleco:int
    id_idic:int
    modelo:str
    stock:Optional[bool]
    vencimiento_funda:datetime
    vencimiento_panel:datetime
    
    
class Ventas(BaseModel):
    id_venta:int
    id_producto:int
    factura:str
    gd:str
    id_cliente:int
    id_vendedor:int
    comentarios:str


class Muestras(BaseModel):
    id_muestra:int
    id_producto:int
    id_cliente:int
    id_vendedor:int

    
    
class Clientes(BaseModel):
    id_cliente:int
    nombre:str
    direccion:str
    correo:str
    telefono:str
    comentarios:str
    
    
class Usuarios(BaseModel):
    user:str
    password:str
    rol:str
    

class Devoluciones(BaseModel):
    id_devolucion:int
    id_venta:int
    id_chaleco:int
    fecha_devolucion:datetime
    motivo:str
    estado:str

