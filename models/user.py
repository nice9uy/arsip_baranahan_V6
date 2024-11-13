from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    nip: str
    nama: str
    password: str
    is_active: bool
    join_date: int = int(datetime.timestamp(datetime.now()))
    update_date: int = int(datetime.timestamp(datetime.now()))


class User(BaseModel):
    id: str
    nip: str


class Item(BaseModel):
    nip: str
    nama: str
    is_active: bool


class ItemInDB(Item):
    id: str
