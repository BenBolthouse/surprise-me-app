from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import sqlalchemy as sa


from .db import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    # Properties
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    share_location = db.Column(db.Boolean, default=False)
    coord_lat = db.Column(sa.types.DECIMAL(precision=9, scale=6), nullable=False)
    coord_long = db.Column(sa.types.DECIMAL(precision=8, scale=6), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now())

    # Associations
    _connections = db.relationship("UserConnection",
                                   backref="users",
                                   cascade="all, delete-orphan")
    _notifications = db.relationship("UserNotification",
                                     backref="users",
                                     cascade="all, delete-orphan")
    _payment_methods = db.relationship("UserPaymentMethods",
                                       backref="users",
                                       cascade="all, delete-orphan")

    # Getters setters
    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def password_is_valid(self, password):
        return check_password_hash(self.password, password)

    # TODO implement association getters and setters

    # TODO implement scopes while creating routes
