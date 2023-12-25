import structlog
from core.logger_setup import configure_structlog
from core.settings import Settings
from db.postgres import get_connection_pool
from db.rabbit import get_channel_pool
from dependency_injector import containers, providers
from notification_provider import SMTPProvider, TestProvider
from user_provider import UserProvider


class Container(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)

    logging = providers.Resource(
        configure_structlog,
        settings().json_logging_level,
        settings().console_logging_level,
    )

    smtp_provider: providers.Singleton[SMTPProvider] = providers.Singleton(
        SMTPProvider,
        smtp_host=settings().smtp.host,
        smtp_port=settings().smtp.port,
        login=settings().smtp.login,
        password=settings().smtp.password,
        logger=structlog.get_logger("smtp_provider"),
    )

    test_provider: providers.Singleton[TestProvider] = providers.Singleton(
        TestProvider,
        logger=structlog.get_logger("test_provider"),
    )

    postgres_connection_pool: providers.Factory = providers.Factory(get_connection_pool)
    rabbit_channel_pool: providers.Singleton = providers.Singleton(get_channel_pool)

    user_provider: providers.Singleton[UserProvider] = providers.Singleton(
        UserProvider,
        logger=structlog.get_logger("user_provider"),
        connection_pool=postgres_connection_pool,
    )
