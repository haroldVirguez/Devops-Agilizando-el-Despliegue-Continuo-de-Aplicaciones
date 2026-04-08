"""Imprime un access token JWT para Postman (mismo secreto que JWT_SECRET_KEY de la app)."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

# Solo hace falta JWT_SECRET_KEY para firmar; SQLite evita depender de Postgres en .env.
os.environ["DATABASE_URL"] = "sqlite:///dev.db"

os.environ.setdefault("FLASK_ENV", "development")
os.environ.setdefault("JWT_SECRET_KEY", "dev-jwt-secret-change-me")

from app import create_app
from flask_jwt_extended import create_access_token

app = create_app("development")
with app.app_context():
    print(create_access_token(identity="postman-client"))
