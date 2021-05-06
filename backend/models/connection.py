from datetime import datetime


from .mixins.Entity import EntityMixin
from .db import db
from .User import User
from .Message import Message


class Connection(db.Model, EntityMixin):
    __tablename__ = "connections"

    requestor_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False)
    approver_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False)
    approved_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)

    def approve(self):
        self.approved_at = datetime.now()

    def deny(self):
        self.deleted_at = datetime.now()

    def leave(self):
        self.deleted_at = datetime.now()
        self.approved_at = None

    def rejoin(self, user_id):
        self.deleted_at = None
        self.approved_at = None

        if user_id != self.requestor_id:
            self.approver_id = self.requestor_id
            self.requestor_id = user_id

    def other_user(self, user_id):
        '''
        Returns the other user of the connection with a given user ID.
        '''
        other_user_id = self.requestor_id if self.approver_id == user_id else self.approver_id

        return User.query.get(other_user_id)
    def user_is_member(self, user_id):
        '''
        Returns true if user is a requestor or approver.
        '''
        return user_id == self.requestor_id or self.approver_id

    def to_dict(self, user_id):
        '''
        Returns dictionary representation in the context of the current user.
        '''
        return {
            **self.entity_to_dict(),
            "requestor_id": self.requestor_id,
            "other_user": self.other_user(user_id),
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
        }

    def __init__(self, requestor_id, approver_id):
        self.requestor_id = requestor_id
        self.approver_id = approver_id
