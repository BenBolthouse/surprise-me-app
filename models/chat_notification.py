from .db import db


class ChatNotification(db.Model):
    def __init__(self, config_object):
        self.sender_user_id = config_object["sender_user_id"]
        self.user_connection_id = config_object["user_connection_id"]
        self.notification_type = config_object["notification_type"]
        self.hook = config_object["hook"]
        self.body = config_object["body"]

    # ** «««««««««««««««« Mapped Properties »»»»»»»»»»»»»»»» **

    __tablename__ = "chat_notifications"

    id = db.Column(
        db.Integer,
        primary_key=True)
    user_connection_id = db.Column(
        db.Integer,
        db.ForeignKey('user_connections.id'),
        nullable=False)
    sender_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    notification_type = db.Column(
        db.String,
        nullable=False)
    hook = db.Column(
        db.String,
        default="")
    body = db.Column(
        db.String,
        nullable=False)
    active = db.Column(
        db.Boolean,
        nullable=False,
        default=True)
    deleted = db.Column(
        db.Boolean,
        nullable=False,
        default=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())

    # ** «««««««««««««««« Scopes »»»»»»»»»»»»»»»» **

    def to_json(self):
        return {
            "id": self.id,
            "userConnectionId": self.user_connection_id,
            "senderUserId": self.sender_user_id,
            "type": self.notification_type,
            "hook": self.hook,
            "body": self.body,
            "active": self.active,
            "deleted": self.deleted,
            "createdAt": self.created_at,
        }
