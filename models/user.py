from flask import jsonify
from flask_login import UserMixin, current_user
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.security import generate_password_hash, check_password_hash


from .db import db
from .purchase import Purchase
from .user_connection import UserConnection
from .chat_message import ChatMessage


class User(db.Model, UserMixin):
    def __init__(self, config_object):
        self.password = config_object["password"]
        self.first_name = config_object["first_name"]
        self.last_name = config_object["last_name"]
        self.email = config_object["email"]
        self.share_location = config_object["share_location"]
        self.coord_lat = config_object["coord_lat"]
        self.coord_long = config_object["coord_long"]

    # ** «««««««««««««««« Mapped Properties »»»»»»»»»»»»»»»» **

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

    # ** «««««««««««««««« Scopes »»»»»»»»»»»»»»»» **

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "shareLocation": self.share_location,
            "coordLat": self.coord_lat,
            "coordLong": self.coord_long,
            "notifications": [x.to_json() for x in self.notifications],
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

    def to_json_connections(self):
        return {
            "connections": [x.to_json() for x in self.connections],
        }

    def to_json_without_coordinates(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "share_location": self.share_location,
            "coord_lat": self.coord_lat,
            "coord_long": self.coord_long,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    # ** «««««««««««««««« Associations »»»»»»»»»»»»»»»» **

    _purchases = db.relationship(
        "Purchase",
        backref="users",
        foreign_keys=[Purchase.sender_user_id],
        cascade="all, delete")
    _notifications = db.relationship(
        "UserNotification",
        backref="users",
        cascade="all, delete")
    _payment_methods = db.relationship(
        "UserPaymentMethod",
        backref="users",
        cascade="all, delete")
    _requested_connections = db.relationship(
        "UserConnection",
        back_populates="_requestor_user",
        foreign_keys=[UserConnection.requestor_user_id],
        cascade="all, delete")
    _received_connections = db.relationship(
        "UserConnection",
        back_populates="_recipient_user",
        foreign_keys=[UserConnection.recipient_user_id],
        cascade="all, delete")
    _chat_messages = db.relationship(
        "ChatMessage",
        back_populates="_sender_user",
        foreign_keys=[ChatMessage.sender_user_id],
        cascade="all, delete")

    # ** «««««««««««««««« Getters and Setters »»»»»»»»»»»»»»»» **

    # «««««««« Password »»»»»»»»

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    # «««««««« Connections »»»»»»»»

    @property
    def connections(self):
        all_connections = [*self._requested_connections,
                           *self._received_connections]
        return all_connections

    @connections.setter
    def connections(self, connection):
        self._requested_connections.append(connection)

    # «««««««« Notifications »»»»»»»»

    @property
    def notifications(self):
        return self._notifications

    @notifications.setter
    def notifications(self, notification):
        self._notifications.append(notification)

    # ** «««««««««««««««« Static Class Methods »»»»»»»»»»»»»»»» **

    @staticmethod
    def email_address_is_unique(email):
        user = User.query.filter(User.email == email).first()
        if user is not None:
            raise BadRequest(response={
                "message": "The requested email is already in use.",  # noqa
            })
        return user

    @staticmethod
    def get_by_id(id):
        user = User.query.filter(User.id == id).first()
        if user is None:
            raise NotFound(response={
                "message": "A user was not found with the provided id.",  # noqa
            })
        return user

    @staticmethod
    def get_by_email(email):
        user = User.query.filter(User.email == email).first()
        if user is None:
            raise NotFound(response={
                "message": "A user was not found with the provided email.",  # noqa
            })
        return user

    # ** «««««««««««««««« Instance Methods »»»»»»»»»»»»»»»» **

    def update(self, config_object):
        self.email_address_is_unique(config_object["email"])
        self.first_name = config_object["first_name"] or self.first_name
        self.last_name = config_object["last_name"] or self.last_name
        self.email = config_object["email"] or self.email
        self.coord_lat = config_object["coord_lat"] or self.coord_lat
        self.coord_long = config_object["coord_long"] or self.coord_long
        self.share_location = (True
                               if config_object["share_location"] is True
                               else False)

        return True

    def password_is_valid(self, password):
        if not check_password_hash(self.password, password):
            raise BadRequest(response={
                "message": "Password is incorrect."
            })
        return True

    def other_user_is_a_connection(self, other_user_id):
        for i in self.connections:
            req_user = i.requestor_user_id == other_user_id
            rec_user = i.recipient_user_id == other_user_id
            if req_user or rec_user:
                return i
        raise BadRequest(response={
            "message": "Other user is not connected to session user.",  # noqa
        })

    def other_user_is_not_a_connection(self, other_user_id):
        for i in self.connections:
            req_user = i.requestor_user_id == other_user_id
            rec_user = i.recipient_user_id == other_user_id
            if req_user or rec_user:
                raise BadRequest(response={
                    "message": "Other user is already connected to session user.",  # noqa
                })
        return True

    def add_connection(self, connection):
        self._requested_connections.append(connection)
        return True

    def add_notification(self, notification):
        self._notification.append(notification)
        return True
