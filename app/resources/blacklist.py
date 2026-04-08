from datetime import datetime, timezone

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import BlacklistEntry
from app.schemas import blacklist_create_schema


def _utcnow():
    return datetime.now(timezone.utc)


def get_client_ip():
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or ""


def _post_result(email, message, success=True):
    return {"success": success, "message": message, "email": email}


class BlacklistCollectionResource(Resource):
    @jwt_required
    def post(self):
        raw = request.get_json(force=True, silent=True)
        if raw is None:
            return {"errors": {"_schema": ["Invalid or missing JSON body"]}}, 400
        try:
            data = blacklist_create_schema.load(raw)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        now = _utcnow()
        ip = get_client_ip()
        email_key = data["email"]
        existing = BlacklistEntry.query.get(email_key)

        try:
            if existing is None:
                entry = BlacklistEntry(
                    email=email_key,
                    app_uuid=str(data["app_uuid"]),
                    blocked_reason=data.get("blocked_reason"),
                    client_ip=ip,
                    created_at=now,
                    updated_at=now,
                )
                db.session.add(entry)
                db.session.commit()
                return _post_result(
                    email_key, "The email was added to the global blacklist."
                ), 201

            existing.app_uuid = str(data["app_uuid"])
            if "blocked_reason" in raw:
                existing.blocked_reason = data.get("blocked_reason")
            existing.client_ip = ip
            existing.updated_at = now
            db.session.commit()
            return _post_result(
                email_key, "The email blacklist entry was updated."
            ), 200
        except SQLAlchemyError:
            db.session.rollback()
            return _post_result(
                email_key, "The blacklist entry could not be saved.", success=False
            ), 500


class BlacklistByEmailResource(Resource):
    @jwt_required
    def get(self, email):
        entry = BlacklistEntry.query.get(email)
        if entry is None:
            return {"blacklisted": False, "blocked_reason": None}, 200
        return {"blacklisted": True, "blocked_reason": entry.blocked_reason}, 200
