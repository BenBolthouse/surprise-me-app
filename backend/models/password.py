from werkzeug.security import generate_password_hash, check_password_hash


from .mixins.Entity import EntityMixin
from .db import db


class Password(db.Model, EntityMixin):
    __tablename__ = "passwords"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False)
    value = db.Column(
        db.String,
        nullable=False)

    def set_value(self, value):
        return generate_password_hash(value)

    def validate(self, value):
        return check_password_hash(self.value, value)

    def __init__(self, user_id, value):
        self.user_id = user_id
        self.value = self.set_value(value)
