from marshmallow import Schema, fields

from utils import hash_password


class UserSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.Method(required=True, deserialize='load_password')

    created_at = fields.DateTime(dump_only=True)
    update_at = fields.DateTime(dump_only=True)

    def load_password(self, value):
        return hash_password(value)
