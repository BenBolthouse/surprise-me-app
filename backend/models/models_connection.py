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
    expired_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)

    # Model Relationships -----------------------
    messages = db.relationship(
        Message,
        backref="connections",
        foreign_keys=[Message.connection],
        cascade="all, delete")

    # Methods ------------------------------------
    def other_user(self, user_id):
        """ Returns the other user of the connection with a given user ID."""
        if self.requestor.id == user_id:
            return self.recipient
        elif self.recipient.id == user_id:
            return self.requestor
        else:
            # this condition means a wrong user id was provided
            raise Exception("The user ID provided is not associated with the connection.")
