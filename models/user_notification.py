from .db import db


class UserNotification(db.Model):
    def __init__(self, config_object):
        self.user_id = config_object["user_id"]
        self.notification_type = config_object["notification_type"]
        self.hook = config_object["hook"]
        self.body = config_object["body"]

    # ** «««««««««««««««« Mapped Properties »»»»»»»»»»»»»»»» **

    __tablename__ = "user_notifications"

    id = db.Column(
        db.Integer,
        primary_key=True)
    user_id = db.Column(
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
    read_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)
    dismissed_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())

    # ** «««««««««««««««« Scopes »»»»»»»»»»»»»»»» **

    def to_json(self, includes):
        return {
            "id": self.id,
            "type": self.notification_type,
            "hook": self.hook,
            "body": self.body,
            "readAt": self.read_at,
            "dismissedAt": self.dismissed_at,
            "createdAt": self.created_at,
        }
