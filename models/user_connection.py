from datetime import datetime
from werkzeug.exceptions import BadRequest, NotFound, Forbidden


from .db import db


class UserConnection(db.Model):
    def __init__(self, recipient_user_id):
        self.recipient_user_id = recipient_user_id

    __tablename__ = "user_connections"

    # Properties
    id = db.Column(
        db.Integer,
        primary_key=True)
    requestor_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    recipient_user_id = db.Column(
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
    _chat_messages = db.relationship(
        "ChatMessage",
        backref="user_connections",
        cascade="all, delete-orphan")
    _notifications = db.relationship(
        "ChatNotification",
        backref="user_connections",
        cascade="all, delete-orphan")
    _recipient_user = db.relationship(
        "User",
        back_populates="_received_connections",
        foreign_keys=[recipient_user_id])
    _requestor_user = db.relationship(
        "User",
        back_populates="_requested_connections",
        foreign_keys=[requestor_user_id])

    # Getter setter properties
    @property
    def messages(self):
        return self._chat_messages

    @messages.setter
    def messages(self, message):
        self._chat_messages.append(message)

    @property
    def recipient(self):
        return self._recipient_user

    @property
    def requestor(self):
        return self._requestor_user

    # Static methods
    @staticmethod
    def get_by_id(id):
        """
        Get a user connection by id.

        Will raise `werkzeug.errors.NotFound`
        exception if SQLAlchemy cannot find the
        connection with the provided ID.

        param `id` type Integer
        """
        con = UserConnection.query.filter(UserConnection.id == id).first()
        if con is None:
            raise NotFound(response={
                "message": "A connection was not found with the provided id."
            })
        return con

    # Instance methods
    def user_by_id_is_associated(self, user_id):
        """
        Check if the user id provided is assigned to a user
        associated with this connection.

        Will raise `werkzeug.errors.Forbidden` exception if the
        provided id is not associated.

        param `user_id` type Integer
        """
        user_is_requestor = user_id == self.requestor_user_id
        user_is_recipient = user_id == self.recipient_user_id
        if not user_is_requestor and not user_is_recipient:
            raise Forbidden(response={
                "message": "User is not associated with this connection."
            })
            return True

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
            raise Forbidden(response={
                "message": "User is not the requestor for this connection."
            })
        return True

    def user_by_id_is_recipient(self, user_id):
        """
        Check if the user id provided is the
        user id of the recipient.

        Will raise `werkzeug.errors.BadRequest`
        exception if the provided id is not the
        recipient id.

        param `user_id` type Integer
        """
        if user_id != self.recipient_user_id:
            raise Forbidden(response={
                "message": "User is not the recipient for this connection."
            })
        return True

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
        message_list = [m for m in self.messages
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
        message_list.reverse()
        message_list = message_list[offset:offset_quantity]

        if not message_list:
            raise NotFound(response={
                "message": "No messages were found."  # noqa
            })
        return message_list

    def require_establishment(self):
        """
        Assert that the connection is
        established before carrying out an
        action.

        Will raise `werkzeug.errors.BadRequest`
        if the connection is not established.
        """
        if self.established_at is None:
            raise BadRequest(response={
                "message": "Connection is not yet established.",
            })
        return True

    # Scopes
    def to_json(self):
        return {
            "id": self.id,
            "recipientUserId": self.recipient_user_id,
            "recipientFirstName": self.recipient.first_name,
            "recipientLastName": self.recipient.last_name,
        }

    def to_json_as_recipient(self):
        return {
            "id": self.id,
            "requestorUserId": self.requestor_user_id,
            "requestorFirstName": self.requestor.first_name,
            "requestorLastName": self.requestor.last_name,
            "accept": f"/api/connections/{self.id}/accept",
            "deny": f"/api/connections/{self.id}/deny",
        }
