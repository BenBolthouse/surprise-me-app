from datetime import datetime
from sqlalchemy.orm import backref


from .mixins.Entity import EntityMixin
from .mixins.Dismissible import DismissibleMixin
from .db import db


class Notification(db.Model, EntityMixin, DismissibleMixin):
    __tablename__ = "notifications"

    recipient_id = db.Column(
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

    types = {
        "CONNECTION",
        "GIFT",
        "MESSAGE",
        "APP",
    }

    def to_dict(self):
        return {
            **self.entity_to_dict(),
            **self.dismissible_to_dict(),
            "type": self.type,
            "body": self.body,
            "action": self.action,
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

    def __init__(self, type, recipient_id, body, action):
        self.set_type(type)
        self.recipient_id = recipient_id
        self.body = body
        self.action = action
