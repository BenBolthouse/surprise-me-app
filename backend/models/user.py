from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import backref


from .mixins.entity import EntityMixin
from .db import db
from .connection import Connection
from .email import Email
from .notification import Notification
from .password import Password


class User(db.Model, UserMixin, EntityMixin):
    __tablename__ = "users"

    first_name = db.Column(
        db.String(64),
        nullable=False)
    last_name = db.Column(
        db.String(64),
        nullable=False)
    _user_engagement_score = db.Column(
        db.BigInteger,
        name="user_engagement_score",
        nullable=False,
        default=0)

    email_addresses = db.relationship(
        Email,
        backref=backref("users", cascade="all,delete"))
    notifications = db.relationship(
        Notification,
        backref=backref("users", cascade="all,delete"))
    passwords = db.relationship(
        Password,
        backref=backref("users", cascade="all,delete"))

    @property
    def active_email_address(self):
        return next(x for x in self.email_addresses if not x.is_deleted)

    def set_active_email_address(self, value):
        for x in self.email_addresses:
            # This prevents users from creating identical email addresses.
            if x.value == value:
                raise Exception("Email is expired")

            # Invoking this method soft deletes all existing email
            # addresses for the user, including the current active email.
            if not x.is_deleted():
                x.set_deleted_at()

        self.email_addresses.append(Email(value))
        self.set_updated_at()

    @property
    def deleted_email_addresses(self):
        return [x for x in self.email_addresses if x.is_deleted]

    @property
    def unseen_notifications(self):
        return [x for x in self.notifications if not x.is_seen()]

    @property
    def seen_notifications(self):
        return [x for x in self.notifications if x.is_seen()]

    @property
    def dismissed_notifications(self):
        return [x for x in self.notifications if x.dismissed_at is not None]

    @property
    def active_password(self):
        return next(x for x in self.passwords if not x.is_deleted)

    def set_active_password(self, value):
        for x in self.passwords:
            # This prevents users from creating identical email addresses.
            if x.validate(value):
                raise Exception("Password is expired")

            # Invoking this method soft deletes all existing passwords for
            # the user, including the current active password.
            if not x.is_deleted():
                x.set_deleted_at()

        self.passwords.append(Password(value))
        self.set_updated_at()

    @property
    def deleted_passwords(self):
        return [x for x in self.passwords if x.is_deleted]

    @property
    def user_engagement_score(self):
        return self._user_engagement_score

    def set_user_engagement_score(self, points):
        self._user_engagement_score += points

        if self._user_engagement_score < 0:
            self._user_engagement_score = 0

    def to_http_response(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.active_email_address,
        }

    def __init__(self, **kwargs):
        self.first_name = kwargs["first_name"]
        self.last_name = kwargs["last_name"]
