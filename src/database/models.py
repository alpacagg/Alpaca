from tortoise import fields
from tortoise.models import Model

class User(Model):
    id_user = fields.IntField(pk=True)

class Ban(Model):
    id_ban = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="bans")
    created_at = fields.DateField()
    reason = fields.CharField(max_length=255, null=True)

class TemporaryBan(Model):
    id_temporary_ban = fields.IntField(pk=True, generated=True)
    ban = fields.ForeignKeyField("models.Ban", related_name="temporary_bans")
    end_date = fields.DateField()

class SupportedGame(Model):
    id_supported_game = fields.IntField(pk=True, generated=True)
    name = fields.CharField(max_length=255)

class Template(Model):
    id_template = fields.IntField(pk=True, generated=True)
    supported_game = fields.ForeignKeyField("models.SupportedGame", related_name="templates")
    link = fields.CharField(max_length=255)
    coord_x = fields.IntField()
    coord_y = fields.IntField()
    canvas = fields.IntField()
    created_at = fields.DateField()

class TemplateUserOwned(Model):
    template = fields.ForeignKeyField("models.Template", related_name="user_owned")
    user = fields.ForeignKeyField("models.User", related_name="owned_templates")

class Server(Model):
    id_server = fields.IntField(pk=True)

class TemplateServerOwned(Model):
    template = fields.ForeignKeyField("models.Template", related_name="server_owned")
    server = fields.ForeignKeyField("models.Server", related_name="owned_templates")

class VoidChannel(Model):
    server = fields.ForeignKeyField("models.Server", related_name="void_channels")
    channel_id = fields.IntField()
    message_id = fields.IntField()

class ServerSettings(Model):
    server = fields.ForeignKeyField("models.Server", related_name="settings")
    admin_role_id = fields.IntField()
