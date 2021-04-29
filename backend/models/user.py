from datetime import datetime
from flask_login import UserMixin


from .mixins.entity import EntityMixin
from .db import db
from .email import Email
from .notification import Notification
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

    email_addresses = db.relationship(
        Email,
        backref="users",
        foreign_keys=[Email.user],
        cascade="all, delete")
    notifications = db.relationship(
        Notification,
        backref="users",
        foreign_keys=[Notification.recipient],
        cascade="all, delete")
    passwords = db.relationship(
        Password,
        backref="users",
        foreign_keys=[Password.user],
        cascade="all, delete")

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value
        self.set_updated_at()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value
        self.set_updated_at()

    @property
    def active_email_address(self):
        return next(x for x in self.email_addresses if not x.is_deleted())

    def set_active_email_address(self, value):
        for x in self.email_addresses:
            # Invoking this method soft deletes all existing email
            # addresses for the user, including the current active email.
            if x.deleted_at is not None:
                x.set_deleted_at()

            # This prevents users from creating identical email addresses.
            if x.value == value:
                raise Exception("Email address already exists for user and is expired")

        self.email_addresses.append(Email(value))
        self.set_updated_at()

    @property
    def expired_email_addresses(self):
        return [x for x in self.email_addresses if x.is_deleted()]

    # @property
    # def unseen_notifications(self):
    #     return [x for x in self.notifications if x.seen_at is None]

    # @property
    # def seen_notifications(self):
    #     return [x for x in self.notifications if x.seen_at is not None]

    # @property
    # def dismissed_notifications(self):
    #     return [x for x in self.notifications if x.dismissed_at is not None]

    # @property
    # def active_password(self):
    #     return next(x for x in self.passwords if x.expired_at is None)

    # @active_password.setter
    # def active_password(self, value):
    #     timestamp = datetime.now()
    #     for x in self.passwords:
    #         if x.expired_at is None:
    #             x.expired_at = timestamp
    #         if x.value == value:
    #             raise Exception("Password already exists for user and is expired")
    #     self.passwords.append(Password(value))
    #     self.updated_at = timestamp

    # @property
    # def expired_passwords(self):
    #     return [x for x in self.passwords if x.expired_at is not None]

    # # Constructor -------------------------------
    # def __init__(self, first_name, last_name,
    #              email, password):
    #     self.first_name = first_name
    #     self.last_name = last_name
