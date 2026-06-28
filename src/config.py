from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from src.logger import logger
from src.exceptions import ConfigurationError

class Settings(BaseSettings):
    sqlcipher_key: str
    sqlite_db_path: str = "local_chronicle.db"
    gguf_model_path: str = "models/Phi-3-mini-4k-instruct-q4.gguf"
    whisper_model_path: str = "models/whisper_base"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

def get_settings() -> Settings:
    try:
        if not Path(".env").exists():
            logger.critical("No .env file found. Application cannot securely boot.")
            raise ConfigurationError(".env file missing")
        return Settings()
    except Exception as e:
        logger.exception("Configuration Validation Failed. Check .env variables.")
        raise ConfigurationError("Invalid or missing environment variables.") from e
