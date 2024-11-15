# from passlib.context import CryptContext
# from ..models.user import UserInDB

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


# def get_user(db, nip: str):
#     if nip in db:
#         user_dict = db[nip]
#         return UserInDB(**user_dict)


from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from .config import db
from ..models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db["users"].find_one({"email": email})
    if user is None:
        raise credentials_exception
    return User(**user)
