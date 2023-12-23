from fastapi import FastAPI
from .routes import example_route

app = FastAPI()

app.include_router(example_route.router)
