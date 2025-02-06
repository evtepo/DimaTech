from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = Field("Wallet API", alias="SERVICE_NAME")
    service_host: str = Field("localhost", alias="SERVICE_HOST")
    service_port: int = Field(8000, alias="SERVICE_PORT")

    pg_name: str = Field("wallet", alias="POSTGRES_DB")
    pg_user: str = Field("postgres", alias="POSTGRES_USER")
    pg_password: str = Field("postgres", alias="POSTGRES_PASSWORD")
    pg_host: str = Field("localhost", alias="POSTGRES_HOST")
    pg_port: int = Field(5432, alias="POSTGRES_PORT")

    token_secret_key: str = Field("nie", alias="TOKEN_SECRET_KEY")
    access_token_expire_in_seconds: int = 60 * 60

    signature_secret_key: str = Field("nie", alias="SIGNATURE_SECRET_KEY")

    @property
    def database_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_name}"


settings = Settings()
