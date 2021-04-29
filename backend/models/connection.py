from .mixins.entity import EntityMixin
from .db import db
from .message import Message


class Connection(db.Model, EntityMixin):
    __tablename__ = "connections"

    requestor = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    recipient = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    approved_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)

    _messages = db.relationship(
        Message,
        backref="connections",
        foreign_keys=[Message.connection],
        cascade="all, delete")

    @property
    def messages(self):
        # only get messages that are not soft deleted
        return [x for x in self._messages if not x.is_deleted()]

    def add_message(self, value):
        self._messages.append(value)

    def other_user(self, user_id):
        '''
        Returns the other user of the connection with a given user ID or raises Exception.
        '''
        return self.requestor.id if self.recipient.id == user_id else self.recipient.id
        raise Exception("The user is not in the connection")

    def user_is_in_connection(self, user_id):
        '''
        Returns true if user is a requestor or recipient or raises Exception.
        '''
        return user_id == self.requestor.id or self.recipient.id
        raise Exception("The user is not in the connection")

    def __init__(self, requestor_id, recipient_id):
        self.requestor = requestor_id
        self.recipient = recipient_id
