import os

import pytest
from flask_jwt_extended import create_access_token

from app import create_app, db


@pytest.fixture
def app():
    os.environ["FLASK_ENV"] = "development"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["JWT_SECRET_KEY"] = "test-secret-key"
    os.environ["SKIP_DB_CREATE_ALL"] = "1"

    app = create_app("development")
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_header(app):
    with app.app_context():
        token = create_access_token(identity="pytest-client")
    return {"Authorization": f"Bearer {token}"}
