from datetime import datetime
from werkzeug.exceptions import BadRequest, NotFound


from .db import db


class UserConnection(db.Model):
    def __init__(self, connection_user_id):
        self.connection_user_id = connection_user_id

    __tablename__ = "user_connections"

    # Properties
    id = db.Column(
        db.Integer,
        primary_key=True)
    requestor_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    connection_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    established_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)

    # Associations
    _messages = db.relationship(
        "ChatMessage",
        backref="user_connections",
        cascade="all, delete-orphan")
    _notifications = db.relationship(
        "ChatNotification",
        backref="user_connections",
        cascade="all, delete-orphan")

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, message):
        self._messages.append(message)

    def to_json_on_create(self):
        return {
            "id": self.id,
        }

    # Static methods
    @staticmethod
    def get_by_id(id):
        """
        Get a user connection by id.

        Will raise `werkzeug.errors.NotFound`
        exception if SQLAlchemy cannot find the
        user with the provided ID.

        param `id` type Integer
        """
        con = UserConnection.query.filter(UserConnection.id == id).first()
        if con is None:
            raise NotFound(response={
                "message": "A connection was not found with the provided id."
            })
        return con

    # Instance methods
    def user_by_id_is_requestor(self, user_id):
        """
        Check if the user id provided is the
        user id of the requestor.

        Will raise `werkzeug.errors.BadRequest`
        exception if the provided id is not the
        requestor id.

        param `user_id` type Integer
        """
        if user_id != self.requestor_user_id:
            raise BadRequest(response={
                "message": "User is not the requestor for this connection."
            })

    def user_by_id_is_recipient(self, user_id):
        """
        Check if the user id provided is the
        user id of the recipient.

        Will raise `werkzeug.errors.BadRequest`
        exception if the provided id is not the
        recipient id.

        param `user_id` type Integer
        """
        if user_id != self.connection_user_id:
            raise BadRequest(response={
                "message": "User is not the recipient for this connection."
            })

    def get_chat_messages_after_datetime(self, date_time):
        """
        Get all chat messages for this
        connection after the provided datetime
        string.

        param `date_time` type String formatted
        as
        [YYYY]-[mm]-[dd]T[HH]:[MM]:[SS].[ffffff],
        e.g. 2020-03-09T05:36:14.549101
        """
        date_time_format = "%Y-%m-%dT%H:%M:%S.%f"
        date_time_obj = datetime.strptime(date_time, date_time_format)
        message_list = [m.to_json_on_create()
                        for m in self.messages
                        if m.created_at > date_time_obj]
        return message_list

    def get_chat_messages_by_offset(self, offset, quantity):
        """
        Get all chat messages from a reverse
        chronological offset and quantity.

        Will raise `werkzeug.errors.NotFound` if
        the operation yields no messages.

        param `offset` type Integer specifies an
        offset of messages in reverse
        chronological order.

        param `quantity` type Integer specifies
        how many messages to retrieve from the
        index of offset.
        """
        offset_quantity = offset + quantity
        message_list = self.messages.copy()
        message_list = message_list[offset:offset_quantity]

        if not message_list:
            raise NotFound(response={
                "message": "Message offset out of range and yielded no results."  # noqa
            })

        return [m.to_json_on_create() for m in message_list]
