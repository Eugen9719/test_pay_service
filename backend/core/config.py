
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"  # Базовая строка API
    SECRET_KEY: str = ""
    SECRET_PAYMENT_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # Время жизни токена доступа (8 дней)
    DOMAIN: str = "localhost"  # Домен приложения
    SERVER_HOST: str = 'http://127.0.0.1:8010'

    PROJECT_NAME: str = "KOROBKA API"
    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@test_pay_db:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    password_reset_jwt_subject: str = 'present'


settings = Settings()
