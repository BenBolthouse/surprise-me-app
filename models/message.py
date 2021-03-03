from .db import db


class Message(db.Model):
    __tablename__ = "messages"

    # Properties
    id = db.Column(db.Integer, primary_key=True)
    user_connection_id(db.Integer,
                       db.ForeignKey('user_connections.id'),
                       nullable=False)
    sender_user_id = db.Column(db.Integer, nullable=False)
    body = db.Column(db.String, nullable=False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    updated = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # TODO implement association getters and setters

    # TODO implement scopes while creating routes
