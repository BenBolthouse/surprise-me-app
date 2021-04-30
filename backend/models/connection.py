from datetime import datetime


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
    _approved_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)

    _messages = db.relationship(
        Message,
        backref="connections",
        foreign_keys=[Message.connection],
        cascade="all, delete")

    @property
    def approved_at(self):
        return self._approved_at

    @property
    def messages(self):
        # only get messages that are not soft deleted
        return [x for x in self._messages if not x.is_deleted()]

    def approve(self):
        self._approved_at = datetime.now()

    def deny(self):
        self._deleted_at = datetime.now()

    def leave(self):
        self._deleted_at = datetime.now()

    def is_pending_approval(self):
        self._approved_at is None

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

    def to_http_response(self, user_id):
        '''
        Returns http-ready data in the context of the current user.
        '''
        return {
            "id": self.id,
            "pending": self.is_pending_approval(),
            "user": self.other_user(user_id),
            "since": self.approved_at,
        }

    def __init__(self, requestor_id, recipient_id):
        self.requestor = requestor_id
        self.recipient = recipient_id
