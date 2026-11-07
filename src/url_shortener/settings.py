from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    title: str = "URL Shortener"
    debug: bool = True
    public_base_url: str


class DatabaseSettings(BaseSettings):
    db_host: str
    db_port: int
    db_user_name: str
    db_password: str
    db_name: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user_name}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class UrlSettings(BaseSettings):
    url_ttl_days: int
    short_code_max_retries: int

    # Must match the short_code column length in the database schema.
    short_code_length: int = 16


class Settings(AppSettings, DatabaseSettings, UrlSettings):
    pass


settings = Settings()  # type: ignore[call-arg]
