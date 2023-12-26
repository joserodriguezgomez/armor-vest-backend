from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
import os

# Primero, cargar las variables de entorno desde .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)



from .routes import producto_routes
from .routes import ventas
from .routes import Idic
from .routes import devoluciones
from .routes import chalecos



app = FastAPI()
app.include_router(producto_routes.router, prefix= "/api")
app.include_router(ventas.router, prefix= "/api")
app.include_router(Idic.router, prefix= "/api")
app.include_router(devoluciones.router, prefix= "/api")
app.include_router(chalecos.router, prefix= "/api")

