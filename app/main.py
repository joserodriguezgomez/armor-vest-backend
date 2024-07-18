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

# origins = [
#     "*"
#     # "https://armor-vest-front-ffa4d67fd0e2.herokuapp.com",
#     # "http://localhost:3000",  # Asume que tu frontend está en localhost:3000
#     # "http://localhost:8080",  # Otro ejemplo de origen que podría ser tu frontend
#     # # Agrega cualquier otro origen necesario
# ]



# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # Lista de orígenes permitidos
#     allow_credentials=True,
#     allow_methods=["*"],  # Permite todos los métodos
#     allow_headers=["*"],  # Permite todos los encabezados
# )



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(ventas.router, prefix= "/api")
app.include_router(products.router, prefix= "/api")
app.include_router(batch_input.router, prefix= "/api")
