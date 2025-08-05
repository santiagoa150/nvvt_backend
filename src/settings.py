import os
from dotenv import load_dotenv
from pydantic import Field, AnyUrl
from pydantic_settings import BaseSettings

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))


class Settings(BaseSettings):
    mongodb_uri: AnyUrl = Field(..., validation_alias="MONGODB_URI")
    mongodb_database: str = Field(..., validation_alias="MONGODB_DATABASE")
    nova_venta_user_agent: str = Field(..., validation_alias="NOVAVENTA_USER_AGENT")
    nova_venta_referer: str = Field(..., validation_alias="NOVAVENTA_REFERER")


settings = Settings()
