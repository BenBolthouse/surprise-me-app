from .db import db


class UserConnection(db.Model):
    __tablename__ = "user_connections"

    # Properties
    id = db.Column(db.Integer, primary_key=True)
    requestor_user_id = db.Column(db.Integer,
                                  db.ForeignKey('users.id'),
                                  nullable=False)
    connection_user_id = db.Column(db.Integer,
                                   db.ForeignKey('users.id'),
                                   nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    established_at = db.Column(db.DateTime, nullable=True, default=None)

    # Associations
    _messages = db.relationship("ChatMessage",
                                backref="user_connections",
                                cascade="all, delete-orphan")
    _notifications = db.relationship("ChatNotification",
                                     backref="user_connections",
                                     cascade="all, delete-orphan")

    # TODO implement association getters and setters

    # TODO implement scopes while creating routes
