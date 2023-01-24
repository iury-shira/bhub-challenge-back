from fastapi import FastAPI
from . import models
from .database import engine
from .routers import clients

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(clients.router)