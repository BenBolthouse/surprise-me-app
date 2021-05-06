from datetime import datetime
from sqlalchemy.orm import backref


from .mixins.Entity import EntityMixin
from .mixins.Dismissible import DismissibleMixin
from .db import db


class Notification(db.Model, EntityMixin, DismissibleMixin):
    __tablename__ = "notifications"

    _recipient_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        name="recipient_id",
        nullable=False)
    _body = db.Column(
        db.String(255),
        nullable=False,
        name="body",
        default="")
    _action = db.Column(
        db.String(255),
        nullable=False,
        name="action",
        default="")

    _types = {
        "CONNECTION",
        "GIFT",
        "MESSAGE",
        "APP",
    }

    _recipient = db.relationship(
        "User",
        backref=backref("users", cascade="all,delete"))

    @property
    def body(self):
        return self._body

    @property
    def action(self):
        return self._action

    @property
    def recipient(self):
        return self._recipient

    def to_dict(self):
        return {
            **self._entity_to_dict()(),
            **self._dismissible_to_dict(),
            "type": self._type,
            "body": self._body,
            "action": self._action,
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
        self._set_type(type)
        self._recipient_id = recipient_id
        self._body = body
        self._action = action
