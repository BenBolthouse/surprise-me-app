from .mixins.entity import EntityMixin
from .db import db


class Email(db.Model, EntityMixin):
    __tablename__ = "email_addresses"

    user = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        ondelete="CASCADE",
        nullable=False)
    value = db.Column(
        db.String(255),
        nullable=False,
        unique=True)
    verified = db.Column(
        db.Boolean,
        nullable=False,
        default=False)

    def __init__(self, value):
        self.value = value
