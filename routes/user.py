# from datetime import timedelta
# from typing import Annotated
# from fastapi import APIRouter, HTTPException, Depends, status
# from fastapi.security import OAuth2PasswordRequestForm

# # from .config.security import authenticate_user, create_access_token, get_current_active_user
# from ..config.security import (
#     authenticate_user,
#     create_access_token,
#     get_current_active_user,
# )
# from ..models.user import User
# from ..config.db import get_collection
# from pymongo.collection import Collection
# from ..config.config import settings
# from ..models.user import Token

# router_user = APIRouter(prefix="/user", tags=["USER"])


# @router_user.get("/")
# async def get_all_user(collection: Collection = Depends(get_collection)):
#     user = collection.find()
#     return all_user(user)


# @router_user.post("/")
# async def add_user(users: User, collection: Collection = Depends(get_collection)):
#     try:
#         post_user = collection.insert_one(dict(users))
#         return {"status_code": 200, "id": str(post_user.inserted_id)}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Ada yang Error {e}")from datetime import timedelta
# from typing import Annotated
# from fastapi import APIRouter, HTTPException, Depends, status
# from fastapi.security import OAuth2PasswordRequestForm

# # from .config.security import authenticate_user, create_access_token, get_current_active_user
# from ..config.security import (
#     authenticate_user,
#     create_access_token,
#     get_current_active_user,
# )
# from ..models.user import User
# from ..config.db import get_collection
# from pymongo.collection import Collection
# from ..config.config import settings
# from ..models.user import Token

# router_user = APIRouter(prefix="/user", tags=["USER"])


# @router_user.put("/{user_id}")
# async def update_user(
#     user_id: str, user_update: User, collection: Collection = Depends(get_collection)
# ):
#     try:
#         id = ObjectId(user_id)
#         user_exist = collection.find_one({"_id": id})
#         if not user_exist:
#             return HTTPException(status_code=404, detail="User tidak ditemukan")
#         user_update.update_date = datetime.timestamp(datetime.now())
#         collection.update_one({"_id": id}, {"$set": dict(user_update)})
#         return {"status_code": 200, "message": "User Berhasil di update"}

#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Ada yang error : {e}")


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from ..config.auth import create_access_token
from ..schemas.user import UserCreate, UserOut, Token
from ..config import db

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(email: str, password: str):
    user = await db["users"].find_one({"email": email})
    if user and pwd_context.verify(password, user["hashed_password"]):
        return user
    return None

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate):
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    user_data = {"username": user.username, "email": user.email, "hashed_password": hashed_password}
    await db["users"].insert_one(user_data)
    return UserOut(username=user.username, email=user.email)

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["email"]})
    return Token(access_token=access_token, token_type="bearer")
