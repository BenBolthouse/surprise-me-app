from .db import db

from models import Messages


class Connection(db.Model):
    __tablename__ = "connections"

    # Mapping -----------------------------------
    id = db.Column(
        db.Integer,
        primary_key=True)
    requestor = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    recipient = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    approved_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)
    deleted_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)

    # Model Relationships -----------------------
    _messages = db.relationship(
        Message,
        backref="connections",
        foreign_keys=[Message.connection],
        cascade="all, delete")

    # Properties -------------------------------
    @property
    def messages(self):
        # only get messages that are not soft deleted
        return [x for x in self._messages if x.deleted_at is not None]

    @messages.setter
    def messages(self, value):
        self._messages = value

    # Methods ------------------------------------
    def other_user(self, user_id):
        """ Returns the other user of the connection with a given user ID or raises Exception."""
        return self.requestor.id if self.recipient.id == user_id else self.recipient.id
        raise Exception("The user ID provided is not associated with the connection")

    def user_is_requestor_or_recipient(self, user_id):
        """ Returns true if user is a requestor or recipient or raises Exception."""
        return user_id == self.requestor.id or self.recipient.id
        raise Exception("The user ID provided is not associated with the connection")

    # Constructor -------------------------------
    def __init__(self, requestor_id, recipient_id):
        self.requestor = requestor_id
        self.recipient = recipient_id
