from pydantic_settings import BaseSettings
from pymongo import MongoClient


class Settings(BaseSettings):
    MONGO_URI: str
    DATABASE_NAME: str
    COLLECTION_NAME: str
    JWT_SECRET_KEY: str 
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 

    class Config:
        env_file = ".env"


settings = Settings()

client = MongoClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]
collection = db[settings.COLLECTION_NAME]
