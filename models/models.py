from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.UUIDField(primary_key=True)
    email = fields.CharField(max_length=100, unique=True)
    display_name = fields.CharField(max_length=100, null=True)
    created = fields.DatetimeField(auto_now_add=True)
