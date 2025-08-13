import os

from dotenv import load_dotenv
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


class Settings(BaseSettings):

    mongodb_uri: AnyUrl = Field(..., validation_alias="MONGODB_URI")
    mongodb_database: str = Field(..., validation_alias="MONGODB_DATABASE")
    nova_venta_user_agent: str = Field(..., validation_alias="NOVAVENTA_USER_AGENT")
    nova_venta_referer: str = Field(..., validation_alias="NOVAVENTA_REFERER")
    jwt_secret: str = Field(..., validation_alias="JWT_SECRET")
    jwt_expires_in: int = Field(..., validation_alias="JWT_EXPIRATION_IN_MINUTES")
    jwt_refresh_secret: str = Field(..., validation_alias="JWT_REFRESH_SECRET")
    jwt_refresh_expires_in: int = Field(..., validation_alias="JWT_REFRESH_EXPIRATION_IN_MINUTES")


settings = Settings()
