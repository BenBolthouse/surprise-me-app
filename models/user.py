from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import sqlalchemy as sa


from .db import db
from .purchase import Purchase
from .user_connection import UserConnection


class User(db.Model, UserMixin):
    def __init__(self, user_object):
        self.password = user_object["password"]
        self.first_name = user_object["first_name"]
        self.last_name = user_object["last_name"]
        self.email = user_object["email"]
        self.share_location = user_object["share_location"]
        self.coord_lat = user_object["coord_lat"]
        self.coord_long = user_object["coord_long"]

    __tablename__ = "users"

    # Properties
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
    share_location = db.Column(
        db.Boolean,
        default=False)
    coord_lat = db.Column(
        sa.types.DECIMAL(precision=9, scale=6),
        nullable=False)
    coord_long = db.Column(
        sa.types.DECIMAL(precision=8, scale=6),
        nullable=False)
    hashed_password = db.Column(
        db.String(255),
        nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now())

    # Associations
    _purchases = db.relationship(
        "Purchase",
        backref="users",
        foreign_keys=[Purchase.sender_user_id],
        cascade="all, delete-orphan")
    _notifications = db.relationship(
        "UserNotification",
        backref="users",
        cascade="all, delete-orphan")
    _payment_methods = db.relationship(
        "UserPaymentMethod",
        backref="users",
        cascade="all, delete-orphan")
    _connections = db.relationship(
        "UserConnection",
        backref="users",
        foreign_keys=[UserConnection.requestor_user_id],
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

    def to_json_on_create(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "shareLocation": self.share_location,
            "coordLat": str(self.coord_lat),
            "coordLong": str(self.coord_long),
        }

    def to_json_on_login(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
        }

    def to_json_on_session_get(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "shareLocation": self.share_location,
            "coordLat": str(self.coord_lat),
            "coordLong": str(self.coord_long),
        }

    def to_json_on_patch(self):
        return {
            "password": self.password,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "shareLocation": self.share_location,
        }
