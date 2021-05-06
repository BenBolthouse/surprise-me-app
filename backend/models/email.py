from .mixins.Entity import EntityMixin
from .db import db


class Email(db.Model, EntityMixin):
    __tablename__ = "email_addresses"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False)
    value = db.Column(
        db.String(255),
        nullable=False,
        unique=True)
    verified = db.Column(
        db.Boolean,
        nullable=False,
        default=False)

    def to_dict(self):
        return {
            **self.entity_to_dict(),
            "value": self.value,
        }

    def __init__(self, user_id, value):
        self.user_id = user_id
        self.value = value
