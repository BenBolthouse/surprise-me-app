from datetime import datetime


from .mixins.entity import EntityMixin
from .mixins.dismissible import DismissibleMixin
from .db import db


class Notification(db.Model, EntityMixin, DismissibleMixin):
    __tablename__ = "notifications"

    recipient = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False)
    body = db.Column(
        db.String(255),
        nullable=False,
        default="")
    action = db.Column(
        db.String(255),
        nullable=False,
        default="")
    _types = {
        "CONNECTION",
        "GIFT",
        "MESSAGE",
        "APP",
    }

    def to_ws_response(self):
        return {
            "status": "ok",
            "type": "notification",
            "data": {
                "type": self.type,
                "body": self.body,
                "action": self.action,
            }
        }

    def __init__(self, type, **kwargs):
        self.set_type(type)
        self.recipient = kwargs["recipient"]
        self.body = kwargs["body"]
        self.action = kwargs["action"]
