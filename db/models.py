from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    username = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    user_ip = fields.CharField(max_length=255, null=False)
    user_agent = fields.CharField(max_length=255, null=False)
    registered_at = fields.DatetimeField(auto_now_add=True)
    user_links = fields.ReverseRelation["Link"]

    def __str__(self):
        return f"{self.email} | {self.username}"

    class Meta:
        table = "users"


class Link(Model):
    id = fields.IntField(pk=True)
    endpoint_url = fields.CharField(max_length=255)
    xs_url = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    owner = fields.ForeignKeyField("models.User", related_name="links")
    visitors = fields.ReverseRelation["LinkVisit"]

    def __str__(self):
        return f"{self.xs_url} -> {self.endpoint_url} by {str(self.owner)}"

    class Meta:
        table = "links"



class LinkVisit(Model):
    id = fields.IntField(pk=True)
    link = fields.ForeignKeyField("models.Link", related_name="visits")
    ip_address = fields.CharField(max_length=255)
    user_agent = fields.CharField(max_length=255)
    visited_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "link_visits"

