from datetime import datetime


from .mixins.entity import EntityMixin
from .db import db
from .user import User
from .message import Message


class Connection(db.Model, EntityMixin):
    __tablename__ = "connections"

    _requestor_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        name="requestor_id",
        nullable=False)
    _approver_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        name="approver_id",
        nullable=False)
    _approved_at = db.Column(
        db.DateTime,
        nullable=True,
        name="approved_at",
        default=None)

    @property
    def requestor_id(self):
        return self._requestor_id

    @property
    def approver_id(self):
        return self._approver_id

    @property
    def approved_at(self):
        return self._approved_at

    def approve(self):
        self._approved_at = datetime.now()

    def deny(self):
        self._deleted_at = datetime.now()

    def leave(self):
        self._deleted_at = datetime.now()
        self._approved_at = None

    def rejoin(self, user_id):
        self._deleted_at = None
        self._approved_at = None

        if user_id != self.requestor_id:
            self._approver_id = self.requestor_id
            self._requestor_id = user_id

    def other_user(self, user_id):
        '''
        Returns the other user of the connection with a given user ID or raises Exception.
        '''
        other_user_id = self.requestor_id if self.approver_id == user_id else self.approver_id

        return User.query.get(other_user_id).to_public_dict()

        raise Exception("The user is not in the connection")

    def user_is_member(self, user_id):
        '''
        Returns true if user is a requestor or approver or raises Exception.
        '''
        return user_id == self.requestor_id or self.approver_id

        raise Exception("The user is not in the connection")

    def to_dict(self, user_id):
        '''
        Returns dictionary representation in the context of the current user.
        '''
        return {
            **self._entity_to_dict(),
            "other_user": self.other_user(user_id),
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
        }

    def __init__(self, requestor_id, approver_id):
        self._requestor_id = requestor_id
        self._approver_id = approver_id
