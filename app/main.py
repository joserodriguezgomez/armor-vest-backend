from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
import os
from fastapi.middleware.cors import CORSMiddleware

# Primero, cargar las variables de entorno desde .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


from .routes import ventas
from .routes import products
from .routes import batch_input



app = FastAPI()

# Orígenes permitidos
allowed_origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["X-Requested-With", "Content-Type"],
)


app.include_router(ventas.router, prefix= "/api")
app.include_router(products.router, prefix= "/api")
app.include_router(batch_input.router, prefix= "/api")
