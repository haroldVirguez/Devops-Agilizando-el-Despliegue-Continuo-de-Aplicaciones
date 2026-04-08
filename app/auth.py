"""JWT (Flask-JWT-Extended): manager, callbacks y enlace con la aplicación."""

from flask import jsonify
from flask_jwt_extended import JWTManager

jwt = JWTManager()


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(msg="Token has expired"), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify(msg="Invalid token"), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify(msg=error or "Missing Authorization Bearer token"), 401


def init_jwt(app):
    jwt.init_app(app)
