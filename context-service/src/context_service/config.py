from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    fixtures_dir: Path = Path("synthetic/fixtures/historic")
    cdp_replay_fixtures_dir: Path = Path("synthetic/fixtures/cdp")
    stream_injection_default: bool = False
    trino_host: str | None = None


settings = Settings()
