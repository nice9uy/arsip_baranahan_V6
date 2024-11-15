# # app/crud.py
# from pymongo.collection import Collection
# from bson import ObjectId
# from ..models.user import Item, UserCreate
# from ..config.auth import get_password_hash


# def create_user(db, user: UserCreate):
#     hashed_password = get_password_hash(user.password)
#     user_dict = user.model_dump()
#     user_dict["password"] = hashed_password
#     db["users"].insert_one(user_dict)
#     return user


# def create_item(db, item: Item):
#     item_dict = item.dict()
#     result = db["items"].insert_one(item_dict)
#     item_dict["id"] = str(result.inserted_id)
#     return item_dict


# def get_item(db: Collection, item_id: str):
#     return db["items"].find_one({"_id": ObjectId(item_id)})


# def delete_item(db: Collection, item_id: str):
#     db["items"].delete_one({"_id": ObjectId(item_id)})


from passlib.context import CryptContext
from ..config.config import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(email: str, password: str):
    user = await db["users"].find_one({"email": email})
    if user and pwd_context.verify(password, user["hashed_password"]):
        return user
    return None