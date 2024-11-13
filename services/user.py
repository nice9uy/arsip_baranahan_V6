# app/crud.py
from pymongo.collection import Collection
from bson import ObjectId
from .schemas import Item, UserCreate
from .auth import get_password_hash

def create_user(db, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    db["users"].insert_one(user_dict)
    return user

def create_item(db, item: Item):
    item_dict = item.dict()
    result = db["items"].insert_one(item_dict)
    item_dict["id"] = str(result.inserted_id)
    return item_dict

def get_item(db: Collection, item_id: str):
    return db["items"].find_one({"_id": ObjectId(item_id)})

def delete_item(db: Collection, item_id: str):
    db["items"].delete_one({"_id": ObjectId(item_id)})
