from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL","sqlite:///investment_analytics.db")
    log_level: str = os.getenv("LOG_LEVEL","INFO")

settings=Settings()
