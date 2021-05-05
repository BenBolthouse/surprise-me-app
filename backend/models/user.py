from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import backref


from .mixins.entity import EntityMixin
from .db import db
from .email import Email
from .password import Password


class User(db.Model, UserMixin, EntityMixin):
    __tablename__ = "users"

    _first_name = db.Column(
        db.String(64),
        name="first_name",
        nullable=False)
    _last_name = db.Column(
        db.String(64),
        name="last_name",
        nullable=False)
    _bio = db.Column(
        db.String(128),
        name="bio",
        nullable=True,
        default=None)

    _email_addresses = db.relationship(
        "Email",
        backref=backref("users", cascade="all,delete"))
    _notifications = db.relationship(
        "Notification",
        backref=backref("users", cascade="all,delete"))
    _passwords = db.relationship(
        "Password",
        backref=backref("users", cascade="all,delete"))

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def bio(self):
        return self._bio

    @property
    def active_email_address(self):
        return next(x for x in self._email_addresses if not x.is_deleted)

    def set_active_email_address(self, value):
        for x in self._email_addresses:
            # This prevents users from creating identical email addresses.
            if x._value == value:
                raise Exception("Email is expired")

            # Invoking this method soft deletes all existing email
            # addresses for the user, including the current active email.
            if not x.is_deleted:
                x._set_deleted_at()

        self._email_addresses.append(Email(self.id, value))
        self._set_updated_at()

    @property
    def deleted_email_addresses(self):
        return [x for x in self._email_addresses if x.is_deleted]

    @property
    def unseen_notifications(self):
        return [x for x in self._notifications if not x.is_seen]

    @property
    def seen_notifications(self):
        return [x for x in self._notifications if x.is_seen]

    @property
    def dismissed_notifications(self):
        return [x for x in self._notifications if not x.is_dismissed]

    @property
    def active_password(self):
        return next(x for x in self._passwords if not x.is_deleted)

    def set_active_password(self, value):
        for x in self._passwords:
            # This prevents users from creating identical email addresses.
            if x.validate(value):
                raise Exception("Password is expired")

            # Invoking this method soft deletes all existing passwords for
            # the user, including the current active password.
            if not x.is_deleted:
                x._set_deleted_at()

        self._passwords.append(Password(self.id, value))
        self._set_updated_at()

    @property
    def deleted_passwords(self):
        return [x for x in self_.passwords if x.is_deleted]

    def to_dict(self):
        return {
            **self._entity_to_dict(),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.active_email_address.value,
        }

    def to_public_dict(self):
        return {
            "id": self._id,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name
