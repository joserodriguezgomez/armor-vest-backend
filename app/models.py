from pydantic import BaseModel
from typing import Optional

# Define un modelo Pydantic para tus datos
class Producto(BaseModel):
    id: Optional[str]
    nombre: str
    descripcion: str
    precio: float


