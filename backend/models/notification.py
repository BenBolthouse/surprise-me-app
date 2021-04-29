from datetime import datetime


from .mixins.entity import EntityMixin
from .mixins.dismissible import DismissibleMixin
from .db import db


class Notification(db.Model, EntityMixin, DismissibleMixin):
    __tablename__ = "notifications"

    recipient = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    title = db.Column(
        db.String(64),
        nullable=False,
        default="")
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

    def __init__(self, recipient_id, type, title, body, action):
        self.user = recipient_id
        self._type = "APP"
        self.title = title
        self.body = body
        self.action = action
