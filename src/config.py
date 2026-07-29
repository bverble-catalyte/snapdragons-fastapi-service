import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"{name} environment variable is not set")
    return value


class Settings:
    def __init__(self) -> None:
        self._user = get_required_env("DB_USER")
        self._password = get_required_env("DB_PASSWORD")
        self._host = get_required_env("DB_HOST")
        self._port = get_required_env("DB_PORT")
        self._db_name = get_required_env("DB_NAME")
        self._test_db_name = get_required_env("TEST_DB_NAME")

    def build_url(self, db_name: str) -> str:
        return f"postgresql://{self._user}:{self._password}@{self._host}:{self._port}/{db_name}"

    def database_url(self, db_name: str | None = None) -> str:
        return self.build_url(db_name or self._db_name)

    def test_database_url(self, db_name: str | None = None) -> str:
        return self.build_url(db_name or self._test_db_name)


settings = Settings()
