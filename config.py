from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Database settings
    db_dialect: str
    db_api: str
    user_name: str
    user_password: str
    host_name: str
    port: int
    db_name: str

    # Server settings
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    debug: bool = False 

    # Security settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Password hashing
    pwd_schemes: List[str] = ["bcrypt"]
    pwd_deprecated: str = "auto"

    # CORS settings
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

settings = Settings()