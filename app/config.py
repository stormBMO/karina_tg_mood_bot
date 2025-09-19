from dataclasses import dataclass, field
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    admin_ids: list[str] = field(default_factory=lambda: (
        os.getenv("ADMIN_IDS", "").split(",") if os.getenv("ADMIN_IDS") else []
    ))
    db_path: str = os.getenv("DATABASE_PATH", "./data/db.sqlite")

cfg = Config()
if not cfg.bot_token:
    raise RuntimeError("BOT_TOKEN is missing in env")
