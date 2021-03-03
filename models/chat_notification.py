from .db import db


class ChatNotification(db.Model):
    __tablename__ = "chat_notifications"

    # Properties
    id = db.Column(db.Integer, primary_key=True)
    user_connection_id = db.Column(db.Integer,
                                   db.ForeignKey('user_connections.id'),
                                   nullable=False)
    recipient_user_id = db.Column(db.Integer, nullable=False)
    notification_type = db.Column(db.String, nullable=False)
    hook = db.Column(db.String, default="")
    body = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # TODO implement association getters and setters

    # TODO implement scopes while creating routes
