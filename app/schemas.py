from marshmallow import fields, validate
from flask_marshmallow import Marshmallow

ma = Marshmallow()


class BlacklistCreateSchema(ma.Schema):
    email = fields.Email(required=True)
    app_uuid = fields.UUID(required=True)
    blocked_reason = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(max=255),
        missing=None,
    )


blacklist_create_schema = BlacklistCreateSchema()
