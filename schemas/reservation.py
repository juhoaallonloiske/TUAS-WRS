from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema


class ReservationSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    date = fields.Integer(required=True)
    start = fields.Integer(required=True)
    end = fields.Integer(required=True)
    workspaceId = fields.Integer(required=True)
    is_active = fields.Boolean(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'name'])

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data

    @validates('start')
    def validate_start(self, n):
        if n <= 16:
            raise ValidationError('There is no available times before 16.00')
        if n >= 21:
            raise ValidationError('There is no available times after 21.00')
