from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
import os
from fastapi.middleware.cors import CORSMiddleware

# Primero, cargar las variables de entorno desde .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


from .routes import ventas
from .routes import Idic
from .routes import devoluciones
from .routes import chalecos
from .routes import clientes
from .routes import usuarios
from .routes import cargas_masivas




app = FastAPI()

origins = [
    "*",
    "http://localhost:3000",  # Asume que tu frontend está en localhost:3000
    "http://localhost:8080",  # Otro ejemplo de origen que podría ser tu frontend
    # Agrega cualquier otro origen necesario
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista de orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los encabezados
)



app.include_router(ventas.router, prefix= "/api")
app.include_router(Idic.router, prefix= "/api")
app.include_router(devoluciones.router, prefix= "/api")
app.include_router(chalecos.router, prefix= "/api")
app.include_router(clientes.router, prefix= "/api")
app.include_router(usuarios.router, prefix= "/api")
app.include_router(cargas_masivas.router, prefix= "/api")