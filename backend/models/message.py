from datetime import datetime
from sqlalchemy.orm import backref


from .mixins.entity import EntityMixin
from .mixins.dismissible import DismissibleMixin
from .db import db


class Message(db.Model, EntityMixin, DismissibleMixin):
    __tablename__ = "messages"

    _connection_id = db.Column(
        db.Integer,
        db.ForeignKey('connections.id'),
        name="connection_id",
        nullable=False)
    _sender_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        name="sender_id",
        nullable=False)
    _recipient_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        name="recipient_id",
        nullable=False)
    _body = db.Column(
        db.String(),
        name="body",
        nullable=False,
        default="")
    _action = db.Column(
        db.String(255),
        name="action",
        nullable=True,
        default=None)
    _visibility = db.Column(
        db.Boolean,
        name="visibility",
        nullable=False,
        default=True)

    _types = {
        "MESSAGE",
    }

    _sender = db.relationship(
        "User",
        foreign_keys=[_sender_id],
        backref=backref("messages", cascade="all,delete"))

    @property
    def body(self):
        return self._body

    @property
    def sender(self):
        return self._sender.to_public_dict()

    def to_dict(self):
        return {
            **self._entity_to_dict(),
            **self._dismissible_to_dict(),
            "sender": self.sender,
            "body": self.body,
        }

    def __init__(self, connection_id, sender_id, recipient_id, body):
        self._connection_id = connection_id
        self._sender_id = sender_id
        self._recipient_id = recipient_id
        self._type = "MESSAGE"
        self._body = body
