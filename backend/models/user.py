from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import backref


from .mixins.Entity import EntityMixin
from .db import db
from .Email import Email
from .Password import Password


class User(db.Model, UserMixin, EntityMixin):
    __tablename__ = "users"

    first_name = db.Column(
        db.String(64),
        nullable=False)
    last_name = db.Column(
        db.String(64),
        nullable=False)
    bio = db.Column(
        db.String(128),
        nullable=True,
        default=None)
    latitude = db.Column(
        db.Float(precision=5),
        nullable=False,
        default=00.00000)
    longitude = db.Column(
        db.Float(precision=5),
        nullable=False,
        default=000.00000)

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
    def active_email_address(self):
        return next(x for x in self._email_addresses if not x.is_deleted)

    def set_active_email_address(self, value):
        for x in self._email_addresses:
            # This prevents users from creating identical email addresses.
            if x.value == value:
                raise Exception("Email is expired")

            # Invoking this method soft deletes all existing email
            # addresses for the user, including the current active email.
            if not x.is_deleted:
                x._set_deleted_at()

        self._email_addresses.append(Email(self.id, value))
        self.set_updated_at()

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
        self.set_updated_at()

    @property
    def deleted_passwords(self):
        return [x for x in self_.passwords if x.is_deleted]

    def to_dict(self):
        return {
            **self.entity_to_dict(),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.active_email_address.value,
        }

    def to_public_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
