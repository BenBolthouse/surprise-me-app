from flask import jsonify
from flask_login import UserMixin, current_user
from sqlalchemy.orm import raiseload
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from werkzeug.security import generate_password_hash, check_password_hash
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
        db.String(255),
        nullable=False)
    coord_long = db.Column(
        db.String(255),
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
    _requested_connections = db.relationship(
        "UserConnection",
        back_populates="_requestor_user",
        foreign_keys=[UserConnection.requestor_user_id],
        cascade="all, delete-orphan")
    _received_connections = db.relationship(
        "UserConnection",
        back_populates="_recipient_user",
        foreign_keys=[UserConnection.recipient_user_id],
        cascade="all, delete-orphan")

    # Getters setters
    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    @property
    def connections(self):
        all_connections = [*self._requested_connections,
                           *self._received_connections]
        return all_connections

    @connections.setter
    def connections(self, connection):
        self._requested_connections.append(connection)

    @property
    def notifications(self):
        return self._notifications

    @notifications.setter
    def notifications(self, notification):
        self._notifications.append(notification)

    # Static methods

    @staticmethod
    def check_is_email_unique(email):
        """
        Check to see if an email is in use.

        Will raise
        `werkzeug.exceptions.BadRequest` if the
        email is not unique.

        param `email` String
        """
        user = User.query.filter(User.email == email).first()
        if user is not None:
            raise BadRequest(response={
                "message": "The requested email is in use."
            })
        return True

    @staticmethod
    def get_by_id_on_session_user_load(id):
        """
        Special case loader doesn't include
        collections or purchases in loading
        utilizing `SQLAlchemy.orm.raiseload` to
        prevent eager loading potentially huge
        collections.

        param `id` Integer
        """
        user = User.query.options(
            raiseload("_requested_connections"),
            raiseload("_received_connections")
        ).filter(User.id == id).first()
        if user is None:
            raise NotFound(response={
                "message": "A user was not found with the provided id."
            })
        return user

    @staticmethod
    def get_by_id(id):
        """
        Get a user by id and refresh the
        SQLAlchemy session user.

        Will raise `werkzeug.errors.NotFound`
        if a user isn't found.

        param `id` Integer
        """
        user = User.query.filter(User.id == id).first()
        if user is None:
            raise NotFound(response={
                "message": "A user was not found with the provided id."
            })
        # Perform refresh to get raiseload collections
        if not current_user.is_anonymous and current_user.id == user.id:
            db.session.refresh(user)
        return user

    @staticmethod
    def get_by_email(email):
        """
        Get a user by email and refresh the
        SQLAlchemy session user.

        Will raise `werkzeug.errors.NotFound`
        if a user isn't found.

        param `id` Integer
        """
        user = User.query.filter(User.email == email).first()
        if user is None:
            raise NotFound(response={
                "message": "A user was not found with the provided email."
            })
        # Perform refresh to get raiseload collections
        if not current_user.is_anonymous and current_user.id == user.id:
            db.session.refresh(user)
        return user

    @staticmethod
    def is_email_unique(email):
        user = User.query.filter(User.email == email).first()
        if user is not None:
            raise BadRequest(response={
                "message": "Email is in use."
            })

    # Instance methods
    def password_is_valid(self, password):
        """
        Check if a string is a valid password.

        param `password` String
        """
        if not check_password_hash(self.password, password):
            raise BadRequest(response={
                "message": "Password is incorrect."
            })
        return True

    def user_by_id_is_a_connection(self, id):
        for i in self.connections:
            req_user = i.requestor_user_id == id
            rec_user = i.recipient_user_id == id
            if req_user or rec_user:
                raise BadRequest(response={
                    "message": "Connection request already exists for this user relationship."  # noqa
                })

    # Scopes
    def to_json_on_create(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "shareLocation": self.share_location,
        }

    def to_json_on_login(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "shareLocation": self.share_location,
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
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "shareLocation": self.share_location,
            "coordLat": str(self.coord_lat),
            "coordLong": str(self.coord_long),
        }
