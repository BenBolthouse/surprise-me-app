from .db import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(
        db.Integer,
        primary_key=True)
    user = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    type = db.Column(
        db.String(64),
        nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    seen_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)
    dismissed_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)
