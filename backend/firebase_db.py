import os
from pathlib import Path

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

# Ensure environment variables are loaded
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

_BACKEND_DIR = Path(__file__).resolve().parent


def _resolve_credentials_path() -> Path:
    env_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    if env_path:
        p = Path(env_path)
        if not p.is_absolute():
            if (_BACKEND_DIR.parent / p).exists():
                return _BACKEND_DIR.parent / p
            if (_BACKEND_DIR / p).exists():
                return _BACKEND_DIR / p
        return p

    default_file = (
        _BACKEND_DIR
        / "sentiment-analysis-484f4-firebase-adminsdk-fbsvc-3143dc7521.json"
    )
    if default_file.exists():
        return default_file

    matches = list(_BACKEND_DIR.glob("*firebase-adminsdk*.json")) or list(
        _BACKEND_DIR.glob("*service-account*.json")
    )
    if matches:
        return matches[0]

    return default_file


_CREDENTIALS_PATH = _resolve_credentials_path()

try:
    firebase_admin.get_app()
except ValueError:
    if not _CREDENTIALS_PATH.exists():
        raise FileNotFoundError(
            f"Firebase service account key not found at '{_CREDENTIALS_PATH}'. "
            "Please place your Firebase service account JSON key in the 'backend/' directory "
            "or set the FIREBASE_CREDENTIALS_PATH environment variable in your .env file."
        )
    firebase_admin.initialize_app(
        credentials.Certificate(str(_CREDENTIALS_PATH))
    )

db = firestore.client()

