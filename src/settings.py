from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "TALOS"
    # ADMIN_EMAIL: str
    # TECH_EMAIL: str
    # APP_SECRET: str
    authjwt_secret_key: str = "TALOS"

    class Config:
        env_file = "src/.env"
