from fastapi import APIRouter, HTTPException
from ..models import Ventas, VentasIn
from ..database import db
from typing import List
from bson import ObjectId
from fastapi import HTTPException, Depends
import pandas as pd
import numpy as np
from ..auth.auth_handler import oauth2_scheme




router = APIRouter()
ventas_collection = db.ventas
chalecos_collection = db.chalecos
idic_collection = db.idic
cliente_collection = db.clientes


@router.get("/ventas/")
async def crear_venta(token:str = Depends(oauth2_scheme)):
    print(token)
    return "hola mundo"
