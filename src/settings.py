import os

from dotenv import load_dotenv
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


class Settings(BaseSettings):

    mongodb_uri: AnyUrl = Field(..., validation_alias="MONGODB_URI")
    mongodb_database: str = Field(..., validation_alias="MONGODB_DATABASE")
    novaventa_product_search_url: str = Field(..., validation_alias="NOVAVENTA_PRODUCT_SEARCH_URL")
    novaventa_product_image_url: str = Field(..., validation_alias="NOVAVENTA_PRODUCT_IMAGE_URL")
    campaign_files_storage_path: str = Field(..., validation_alias="CAMPAIGN_FILES_STORAGE_PATH")
    campaign_files_static_url_prefix: str = Field(
        ..., validation_alias="CAMPAIGN_FILES_STATIC_URL_PREFIX"
    )
    jwt_secret: str = Field(..., validation_alias="JWT_SECRET")
    jwt_expires_in: int = Field(..., validation_alias="JWT_EXPIRATION_IN_MINUTES")
    jwt_refresh_secret: str = Field(..., validation_alias="JWT_REFRESH_SECRET")
    jwt_refresh_expires_in: int = Field(..., validation_alias="JWT_REFRESH_EXPIRATION_IN_MINUTES")


settings = Settings()
