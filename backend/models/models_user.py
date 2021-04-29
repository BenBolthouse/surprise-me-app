from datetime import datetime
from flask_login import UserMixin


from .db import db
from models import Email, Notification, Password


class User(db.Model, UserMixin):
    __tablename__ = "users"

    # Mapping -----------------------------------
    id = db.Column(
        db.Integer,
        primary_key=True)
    _first_name = db.Column(
        db.String(64),
        name="last_name",
        nullable=False)
    _last_name = db.Column(
        db.String(64),
        name="last_name",
        nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)
    deleted_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)

    # Model Relationships -----------------------
    email_addresses = db.relationship(
        Email,
        backref="users",
        foreign_keys=[Email.user],
        cascade="all, delete")
    notifications = db.relationship(
        Notification,
        backref="users",
        foreign_keys=[Notification.user],
        cascade="all, delete")
    passwords = db.relationship(
        Password,
        backref="users",
        foreign_keys=[Password.user],
        cascade="all, delete")

    # Properties --------------------------------
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter(self, value)
    def first_name(self, value):
        self._first_name = value
        self.updated_at = datetime.now()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter(self, value)
    def last_name(self, value):
        self._last_name = value
        self.updated_at = datetime.now()

    @property
    def active_email_address(self):
        return next(x for x in self.email_addresses if x.expired_at is None)

    @active_email_address.setter
    def active_email_address(self, value):
        timestamp = datetime.now()
        for x in self.email_addresses:
            if x.expired_at is None:
                x.expired_at = timestamp
            if x.value == value:
                raise Exception("Email address already exists for user and is expired")
        self.email_addresses.append(Email(value))
        self.updated_at = timestamp

    @property
    def expired_email_addresses(self):
        return [x for x in self.email_addresses if x.expired_at is not None]

    @property
    def unseen_notifications(self):
        return [x for x in self.notifications if x.seen_at is None]

    @property
    def seen_notifications(self):
        return [x for x in self.notifications if x.seen_at is not None]

    @property
    def dismissed_notifications(self):
        return [x for x in self.notifications if x.dismissed_at is not None]

    @property
    def active_password(self):
        return next(x for x in self.passwords if x.expired_at is None)

    @active_password.setter
    def active_password(self, value):
        timestamp = datetime.now()
        for x in self.passwords:
            if x.expired_at is None:
                x.expired_at = timestamp
            if x.value == value:
                raise Exception("Password already exists for user and is expired")
        self.passwords.append(Password(value))
        self.updated_at = timestamp

    @property
    def expired_passwords(self):
        return [x for x in self.passwords if x.expired_at is not None]

    # Constructor -------------------------------
    def __init__(self, first_name, last_name,
                 email, password):
        self.first_name = first_name
        self.last_name = last_name
