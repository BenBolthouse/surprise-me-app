from .db import db


class Connection(db.Model):
    __tablename__ = "connections"

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
