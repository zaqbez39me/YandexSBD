from typing import Any, Dict, Optional

from pydantic import BaseSettings, Field, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(env="PROJECT_NAME", default="Yandex Lavka")
    PROJECT_VERSION: str = Field(env="PROJECT_VERSION", default="1.0")

    POSTGRES_SERVER: str = Field(env="POSTGRES_SERVER", default="localhost")
    POSTGRES_USER: str = Field(env="POSTGRES_USER", default="postgres")
    POSTGRES_PASSWORD: str = Field(env="POSTGRES_PASSWORD", default="password")
    POSTGRES_DB: str = Field(env="POSTGRES_DB", default="postgres")
    POSTGRES_PORT: str = Field(env="POSTGRES_PORT", default="5432")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True


settings = Settings()
