from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    apikey: str = Field(
        default="SDS#$WEG@!@#%WE",
        env="APIKEY",
        alias="APIKEY",
    )

    class Config:
        env_file = ".env"


def load_config() -> Config:
    return Config()
