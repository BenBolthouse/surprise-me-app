from datetime import datetime


from .mixins.entity import EntityMixin
from .mixins.dismissible import DismissibleMixin
from .db import db


class Message(db.Model, EntityMixin, DismissibleMixin):
    __tablename__ = "messages"

    connection = db.Column(
        db.Integer,
        db.ForeignKey('connections.id'),
        nullable=False)
    sender = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    recipient = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    _body = db.Column(
        db.String(),
        name="body",
        nullable=False,
        default="")
    action = db.Column(
        db.String(255),
        nullable=True,
        default=None)
    visibility = db.Column(
        db.Boolean,
        nullable=False,
        default=True)
    _types = {
        "MESSAGE",
    }

    @property
    def body(self):
        return self._body

    def set_body(self, value):
        self._body = value
        self.set_updated_at()

    def __init__(self, connection_id, sender_id, recipient_id, body):
        self.connection = connection_id
        self.sender = sender_id
        self.recipient = recipient_id
        self._type = "MESSAGE"
        self._body = body
