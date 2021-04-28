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
    _value = db.Column(
        db.String(255),
        name="value",
        nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    expired_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)

    # Properties --------------------------------
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = generate_password_hash(value)

    def validate(value):
        return check_password_hash(self._value, value)

    # Constructor -------------------------------
    def __init__(self, value):
        self.value = value
