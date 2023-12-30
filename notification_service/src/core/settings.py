from pathlib import Path
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    host: str = Field()
    port: str = Field("5432")
    user: str = Field()
    db_name: str = Field()
    password: str = Field()

    model_config = SettingsConfigDict(env_prefix="notify_postgres_", env_file=".env")


class RabbitSettings(BaseSettings):
    host: str = Field()
    port: str = Field("5672")
    user: str = Field("guest")
    password: str = Field("guest")

    model_config = SettingsConfigDict(env_prefix="notify_rabbit_", env_file=".env")


class SMTPSettings(BaseSettings):
    login: str
    password: str
    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix="notify_smtp_", env_file=".env")


class QueueNameSettings(BaseSettings):
    user_provided: str
    notify_task: str
    dead_letter: str

    model_config = SettingsConfigDict(env_prefix="notify_queue_", env_file=".env")


class Settings(BaseSettings):
    postgres: ClassVar = PostgresSettings()
    rabbit: ClassVar = RabbitSettings()
    smtp: ClassVar = SMTPSettings()
    queue: ClassVar = QueueNameSettings()

    rabbit_url: str = f"amqp://{rabbit.user}:{rabbit.password}@{rabbit.host}:{rabbit.port}/"
    postgres_dsn: str = (
        f"postgres://{postgres.user}:{postgres.password}@{postgres.host}:{postgres.port}/{postgres.db_name}"
    )

    console_logging_level: str = Field("DEBUG")
    json_logging_level: str = Field("ERROR")


settings = Settings()
PROJECT_ROOT = Path(__file__).parent.parent
