from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_version: str
    debug: bool

    db_server: str
    db_name: str
    db_driver: str
    db_trusted_connection: str
    db_trust_server_certificate: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    embedding_model: str

    # ChromaDB
    chroma_db_path: str
    chroma_collection_name: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @computed_field
    @property
    def database_url(self) -> str:
        driver = quote_plus(self.db_driver)

        return (
            f"mssql+pyodbc://@{self.db_server}/{self.db_name}"
            f"?driver={driver}"
            f"&trusted_connection={self.db_trusted_connection}"
            f"&TrustServerCertificate={self.db_trust_server_certificate}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()