import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Path to backend directory and .env
BACKEND_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BACKEND_DIR / ".env"

# Load .env if present
load_dotenv(dotenv_path=ENV_PATH)

class Settings:
    PROJECT_NAME: str = "StoreLab API"
    VERSION: str = "0.1.0"

    # Supabase credentials
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    # Security & Admin
    ADMIN_KEY: str = os.getenv("ADMIN_KEY", "storelab-admin-2026")
    
    # CORS
    RAW_ORIGINS: str = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,https://kyroai-eight.vercel.app"
    )
    
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        return [orig.strip() for orig in self.RAW_ORIGINS.split(",") if orig.strip()]

    # Transactional Email (SMTP)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "StoreLab <no-reply@storelab.dev>")

settings = Settings()
