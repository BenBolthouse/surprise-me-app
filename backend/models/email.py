from .mixins.entity import EntityMixin
from .db import db


class Email(db.Model, EntityMixin):
    __tablename__ = "email_addresses"

    _user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        name="user_id",
        nullable=False)
    _value = db.Column(
        db.String(255),
        name="value",
        nullable=False,
        unique=True)
    _verified = db.Column(
        db.Boolean,
        name="verified",
        nullable=False,
        default=False)

    @property
    def value(self):
        return self._value
    
    def to_dict(self):
        return {
            **self._entity_to_dict(),
            "value": self._value,
        }

    def __init__(self, user_id, value):
        self._user_id = user_id
        self._value = value
