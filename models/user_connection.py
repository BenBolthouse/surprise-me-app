from werkzeug.exceptions import BadRequest, NotFound, Forbidden


from .db import db


class UserConnection(db.Model):
    def __init__(self, config_object):
        self.requestor_user_id = config_object["requestor_user_id"]
        self.recipient_user_id = config_object["recipient_user_id"]

    # ** «««««««««««««««« Mapped Properties »»»»»»»»»»»»»»»» **

    __tablename__ = "user_connections"

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

    # ** «««««««««««««««« Scopes »»»»»»»»»»»»»»»» **

    def to_json(self, user_id):
        user_is_requestor = self.requestor_user_id == user_id
        return {
            "id": self.id,
            "createdAt": self.created_at,
            "establishedAt": self.established_at,
            "otherUser": (self.recipient.to_json_without_coordinates()
                          if user_is_requestor
                          else self.requestor.to_json_without_coordinates()),
            "lastMessage": (self.messages[-1].to_json()
                            if len(self.messages)
                            else None),
        }

    def to_dict(self):
        user_is_requestor = self.requestor_user_id == user_id
        return {
            "id": self.id,
            "created_at": self.created_at,
            "established_at": self.established_at,
            "otherUser": (self.recipient.to_dict()
                          if user_is_requestor
                          else self.requestor.to_dict()),
            "messages": [x.to_dict() for x in self.messages],
            "notifications": [x.to_dict() for x in self.notifications],
        }

    # ** «««««««««««««««« Associations »»»»»»»»»»»»»»»» **

    _chat_messages = db.relationship(
        "ChatMessage",
        backref="user_connections",
        cascade="all, delete")
    _chat_notifications = db.relationship(
        "ChatNotification",
        backref="user_connections",
        cascade="all, delete")
    _recipient_user = db.relationship(
        "User",
        back_populates="_received_connections",
        foreign_keys=[recipient_user_id])
    _requestor_user = db.relationship(
        "User",
        back_populates="_requested_connections",
        foreign_keys=[requestor_user_id])

    # ** «««««««««««««««« Getters and Setters »»»»»»»»»»»»»»»» **

    # «««««««« Chat Messages »»»»»»»»

    @property
    def messages(self):
        sorted(self._chat_messages, key=lambda m: m.id)
        return self._chat_messages

    @messages.setter
    def messages(self, messages):
        self._chat_messages = messages

    # «««««««« Chat Notifications »»»»»»»»

    @property
    def notifications(self):
        return self._chat_notifications

    @notifications.setter
    def notifications(self, notifications):
        self._chat_notifications = notifications

    # «««««««« Requestor User »»»»»»»»

    @property
    def requestor(self):
        return self._requestor_user

    # «««««««« Recipient User »»»»»»»»

    @property
    def recipient(self):
        return self._recipient_user

    # ** «««««««««««««««« Static Class Methods »»»»»»»»»»»»»»»» **

    @staticmethod
    def get_by_id(id):
        con = UserConnection.query.get(id)
        if con is None:
            raise NotFound(response={
                "message": "A connection was not found with the provided id."
            })
        return con

    # ** «««««««««««««««« Instance Methods »»»»»»»»»»»»»»»» **

    def user_is_associated(self, user_id):
        req_user = user_id == self.requestor_user_id
        rec_user = user_id == self.recipient_user_id
        if not req_user and not rec_user:
            raise Forbidden(response={
                "message": "User is not associated with this connection.",  # noqa
            })
        return (self.requestor_user_id
                if rec_user
                else self.recipient_user_id)

    def user_is_requestor(self, user_id):
        if user_id != self.requestor_user_id:
            raise Forbidden(response={
                "message": "User is not the requestor for this connection.",  # noqa
            })
        return True

    def user_is_recipient(self, user_id):
        if user_id != self.recipient_user_id:
            raise Forbidden(response={
                "message": "User is not the recipient for this connection.",  # noqa
            })
        return True

    def require_establishment(self):
        if self.established_at is None:
            raise Forbidden(response={
                "message": "Connection is not yet established.",  # noqa
            })
        return True

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
        if offset == 0:
            message_list = self.messages[-offset_quantity:]
        else:
            message_list = self.messages[-offset_quantity:offset]

        if not message_list:
            raise NotFound(response={
                "message": "No messages were found in the provided range."  # noqa
            })
        return message_list
