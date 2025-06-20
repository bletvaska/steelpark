from functools import cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mqtt_uri: str = 'mqtt://localhost'
    base_topic: str = 'steelpark/iotcorner/tv'
    vlc_host: str = 'localhost'
    vlc_port: int

    model_config = SettingsConfigDict(
        env_prefix='REMOTE_',
        env_file_encoding='utf-8',
        env_file='.env',
    )


@cache
def get_settings() -> Settings:
    return Settings()
