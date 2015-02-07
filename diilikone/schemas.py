from marshmallow import fields, Schema
from marshmallow.validate import Length

from diilikone.models import DealGroup


def validate_deal_group_id(group_id):
    if group_id is None:
        return True
    return DealGroup.query.get(group_id) is not None


class UserSchema(Schema):
    first_name = fields.Str(required=True, validate=Length(max=255))
    last_name = fields.Str(required=True, validate=Length(max=255))
    email = fields.Email(required=True)
    guild = fields.Str(validate=Length(max=100))
    class_year = fields.Str(validate=Length(max=10))


class DealSchema(Schema):
    size = fields.Integer(required=True, validator=lambda x: x % 25 == 0)
    value = fields.Boolean(allow_none=True)
    comment = fields.String(allow_blank=True, allow_none=True)
    salesperson = fields.Nested(UserSchema)


class DealGroupSchema(Schema):
    deal_group_id = fields.UUID(validator=validate_deal_group_id)
    deals = fields.Nested(DealSchema, many=True)
