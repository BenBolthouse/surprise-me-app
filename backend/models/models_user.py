from flask_login import UserMixin


from .db import db
from models import Password, Notification


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True)
    first_name = db.Column(
        db.String(64),
        nullable=False)
    last_name = db.Column(
        db.String(64),
        nullable=False)
    email = db.Column(
        db.String(255),
        nullable=False,
        unique=True)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now())

    passwords = db.relationship(
        Password,
        backref="users",
        foreign_keys=[Password.user],
        cascade="all, delete")
    notifications = db.relationship(
        Notification,
        backref="users",
        foreign_keys=[Notification.user],
        cascade="all, delete")
