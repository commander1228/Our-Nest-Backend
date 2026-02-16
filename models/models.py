from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.UUIDField(primary_key=True)
    email = fields.CharField(max_length=100, unique=True)
    display_name = fields.CharField(max_length=100, null=True)
    created = fields.DatetimeField(auto_now_add=True)
    
    
class Nest(Model):
    id = fields.UUIDField(primary_key=True)
    join_code = fields.CharField(max_length=10, unique=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField(null=True)
    created_by = fields.ForeignKeyField('models.User', related_name='created_nests')
    users = fields.ManyToManyField('models.User', related_name='joined_nests', through='nest_user')
    created = fields.DatetimeField(auto_now_add=True)
