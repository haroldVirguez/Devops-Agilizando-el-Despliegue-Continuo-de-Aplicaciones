from datetime import datetime, timezone

from app import db


def utcnow():
    return datetime.now(timezone.utc)


class BlacklistEntry(db.Model):
    __tablename__ = "blacklist_entries"

    email = db.Column(db.String(255), primary_key=True)
    app_uuid = db.Column(db.String(36), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=True)
    client_ip = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
