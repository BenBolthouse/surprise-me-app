from datetime import datetime
from sqlalchemy.orm import backref


from .mixins.Entity import EntityMixin
from .mixins.Dismissible import DismissibleMixin
from .User import User
from .db import db


class Message(db.Model, EntityMixin, DismissibleMixin):
    __tablename__ = "messages"

    connection_id = db.Column(
        db.Integer,
        db.ForeignKey('connections.id'),
        nullable=False)
    sender_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    recipient_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    body = db.Column(
        db.String(),
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

    types = {
        "MESSAGE",
    }

    @property
    def sender(self):
        user = User.query.get(self.sender_id)

        if not user:
            raise Error("User does not exist")

        return user

    def to_dict(self):
        return {
            **self.entity_to_dict(),
            **self.dismissible_to_dict(),
            "sender": self.sender.to_public_dict(),
            "body": self.body,
        }

    def __init__(self, connection_id, sender_id, recipient_id, body):
        self.connection_id = connection_id
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.type = "MESSAGE"
        self.body = body
