from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env from project root if present
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)

class Settings:
    # Keep the same attribute names used elsewhere in the project
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    @property
    def sqlalchemy_database_url(self) -> str:
        return self.DATABASE_URL

settings = Settings()
