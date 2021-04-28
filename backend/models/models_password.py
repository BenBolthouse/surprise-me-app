from .db import db


class Password(db.Model):
    __tablename__ = "passwords"

    id = db.Column(
        db.Integer,
        primary_key=True)
    user = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    hash = db.Column(
        db.String(255),
        nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    expired_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)
