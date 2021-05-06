from werkzeug.security import generate_password_hash, check_password_hash


from .mixins.Entity import EntityMixin
from .db import db


class Password(db.Model, EntityMixin):
    __tablename__ = "passwords"

    _user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        name="user_id",
        nullable=False)
    _value = db.Column(
        db.String(255),
        name="value",
        nullable=False)

    @property
    def value(self):
        return self._value

    def set_value(self, value):
        return generate_password_hash(value)

    def validate(self, value):
        return check_password_hash(self._value, value)

    def __init__(self, user_id, value):
        self._user_id = user_id
        self._value = self.set_value(value)
