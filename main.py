from fastapi import FastAPI
from .config.db import connect_to_mongodb
from .routes.user import router_user

app = FastAPI()

connect_to_mongodb()

app.include_router(router_user)
