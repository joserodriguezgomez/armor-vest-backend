from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
import os

# Primero, cargar las variables de entorno desde .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)



from .routes import producto_routes
app = FastAPI()
app.include_router(producto_routes.router)
