from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from ..models.user import User
from ..config.db import get_collection
from ..schemas.user import all_user
from bson.objectid import ObjectId
from pymongo.collection import Collection

router_user = APIRouter(prefix="/user", tags=["USER"])


@router_user.get("/")
async def get_all_user(collection: Collection = Depends(get_collection)):
    user = collection.find()
    return all_user(user)


@router_user.post("/")
async def add_user(users: User, collection: Collection = Depends(get_collection)):
    try:
        post_user = collection.insert_one(dict(users))
        return {"status_code": 200, "id": str(post_user.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ada yang Error {e}")


@router_user.put("/{user_id}")
async def update_user(
    user_id: str, user_update: User, collection: Collection = Depends(get_collection)
):
    try:
        id = ObjectId(user_id)
        user_exist = collection.find_one({"_id": id})
        if not user_exist:
            return HTTPException(status_code=404, detail="User tidak ditemukan")
        user_update.update_date = datetime.timestamp(datetime.now())
        collection.update_one({"_id": id}, {"$set": dict(user_update)})
        return {"status_code": 200, "message": "User Berhasil di update"}

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ada yang error : {e}")
