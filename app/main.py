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
from .auth import auth_handler



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_handler.router)
app.include_router(ventas.router, prefix= "/api")
app.include_router(products.router, prefix= "/api")
app.include_router(batch_input.router, prefix= "/api")
