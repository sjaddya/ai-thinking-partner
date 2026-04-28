import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _load_env_file(env_path):
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _to_bool(value, default=False):
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


_load_env_file(BASE_DIR / ".env")


class Config:
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH",
        str(BASE_DIR / "storage" / "app.db"),
    )
    DEBUG = _to_bool(os.environ.get("DEBUG"), default=False)
