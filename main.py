from fastapi import Depends, FastAPI
from .config.auth import get_current_user
from .models.user import User
from .config.db import connect_to_mongodb
from .routes.user import router as auth_router

app = FastAPI()

connect_to_mongodb()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])


@app.get("/protected-route")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}! Welcome to the protected route."}
