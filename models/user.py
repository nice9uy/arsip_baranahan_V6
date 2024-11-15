# from pydantic import BaseModel
# from datetime import datetime


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     username: str | None = None


# class User(BaseModel):
#     nip: str
#     nama: str
#     password: str
#     is_active: bool
#     join_date: int = int(datetime.timestamp(datetime.now()))
#     update_date: int = int(datetime.timestamp(datetime.now()))


# class UserInDB(User):
#     hashed_password: str

# from pydantic import BaseModel, EmailStr

# class UserCreate(BaseModel):
#     username: str
#     email: EmailStr
#     password: str

# class UserOut(BaseModel):
#     username: str
#     email: EmailStr

# class Token(BaseModel):
#     access_token: str
#     token_type: str

from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    disabled: bool = False
