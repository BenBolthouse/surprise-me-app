from werkzeug.security import generate_password_hash, check_password_hash


from .mixins.entity import EntityMixin
from .db import db


class Password(db.Model, EntityMixin):
    __tablename__ = "passwords"

    id = db.Column(
        db.Integer,
        primary_key=True)
    user = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    _value = db.Column(
        db.String(255),
        name="value",
        nullable=False)

    @property
    def value(self):
        return self._value

    def set_value(self, value):
        self._value = generate_password_hash(value)

    def validate(value):
        return check_password_hash(self._value, value)

    def __init__(self, value):
        self.set_value(value)
