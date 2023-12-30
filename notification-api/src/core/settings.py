from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    table_name: str = Field()
    host: str = Field()
    port: str = Field()
    user: str = Field()
    password: str = Field()
    db_name: str = Field()

    model_config = SettingsConfigDict(env_prefix="api_postgres_", env_file=".env")


class RabbitSettings(BaseSettings):
    queue_name: str = Field()
    host: str = Field()
    port: str = Field()
    user: str = Field()
    password: str = Field()

    model_config = SettingsConfigDict(env_prefix="api_rabbit_", env_file=".env")


class Settings(BaseSettings):
    postgres: ClassVar = PostgresSettings()
    rabbit: ClassVar = RabbitSettings()
    rabbit_dsn: str = f"amqp://{rabbit.user}:{rabbit.password}@{rabbit.host}:{rabbit.port}/"
    postgres_dsn: str = (
        f"postgresql://{postgres.user}:{postgres.password}@{postgres.host}:{postgres.port}/{postgres.db_name}"
    )


settings = Settings()
