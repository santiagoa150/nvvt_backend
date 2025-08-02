import os
from dotenv import load_dotenv
from pydantic import Field, AnyUrl
from pydantic_settings import BaseSettings

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))


class Settings(BaseSettings):
    mongodb_uri: AnyUrl = Field(..., env="MONGODB_URI")
    mongodb_database: str = Field(..., env="MONGODB_DATABASE")


settings = Settings()
