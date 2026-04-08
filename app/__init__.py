import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.auth import init_jwt

db = SQLAlchemy()


def create_app(config_name="production"):
    load_dotenv()

    app = Flask(__name__)

    if config_name == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    else:
        app.config.from_object("app.config.ProductionConfig")
        if not app.config.get("SQLALCHEMY_DATABASE_URI"):
            raise ValueError("DATABASE_URL must be set in production")
        if not app.config.get("JWT_SECRET_KEY"):
            raise ValueError("JWT_SECRET_KEY must be set in production")

    app.config.setdefault("JWT_ACCESS_TOKEN_EXPIRES", timedelta(days=365 * 10))

    db.init_app(app)

    from app.schemas import ma as marshmallow_ext

    marshmallow_ext.init_app(app)

    init_jwt(app)

    from app.models import BlacklistEntry  # noqa: F401

    from app.resources.blacklist import BlacklistByEmailResource, BlacklistCollectionResource

    api = Api(app)
    api.add_resource(BlacklistCollectionResource, "/blacklists")
    api.add_resource(BlacklistByEmailResource, "/blacklists/<string:email>")

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    if not os.environ.get("SKIP_DB_CREATE_ALL"):
        with app.app_context():
            db.create_all()

    return app
