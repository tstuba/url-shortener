from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    public_base_url: str


class DataBaseSettings(BaseSettings):
    db_host: str
    db_port: int
    db_user_name: str
    db_password: str
    db_name: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user_name}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class UrlSettings(BaseSettings):
    url_ttl_days: int = 30


class Settings(AppSettings, DataBaseSettings, UrlSettings):
    pass


settings = Settings()  # type: ignore[call-arg]
