from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: int

    @property
    def DATABASE_URL(self):
        return (
            f'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:'
            f'{self.POSTGRES_PASSWORD}@'
            f'{self.DB_HOST}:'
            f'{self.DB_PORT}/'
            f'{self.POSTGRES_DB}'
        )

    model_config = SettingsConfigDict(
        env_file='.env.database'
    )

    # class Config:
    #     env_file = '.env.database'


settings = Settings()
