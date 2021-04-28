from .db import db


class Email(db.Model):
    __tablename__ = "email_addresses"

    # Mapping -----------------------------------
    id = db.Column(
        db.Integer,
        primary_key=True)
    user = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    value = db.Column(
        db.String(255),
        nullable=False)
    verified = db.Column(
        db.Boolean,
        nullable=False,
        default=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    expired_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)

    # Constructor -------------------------------
    def __init__(self, value):
        self.value = value
