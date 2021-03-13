from werkzeug.exceptions import NotFound, BadRequest, Forbidden


from .db import db


class ChatMessage(db.Model):
    def __init__(self, user_connection_id, sender_user_id, body):
        # Do a check on init if the body is empty.
        # Send BadRequest response
        if not body or body == "":
            raise BadRequest(response={
                "message": "The message body cannot be empty."
            })
        self.user_connection_id = user_connection_id
        self.sender_user_id = sender_user_id
        self.body = body

    __tablename__ = "chat_messages"

    # Properties
    id = db.Column(
        db.Integer,
        primary_key=True)
    user_connection_id = db.Column(
        db.Integer,
        db.ForeignKey('user_connections.id'),
        nullable=False)
    sender_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    body = db.Column(
        db.String,
        nullable=False)
    deleted = db.Column(
        db.Boolean,
        nullable=False,
        default=False)
    updated = db.Column(
        db.Boolean,
        nullable=False,
        default=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())

    # Associations
    _sender_user = db.relationship(
        "User",
        back_populates="_chat_messages",
        foreign_keys=[sender_user_id])

    # Getters setters
    @property
    def sender(self):
        return self._sender_user

    # Static methods
    @staticmethod
    def get_by_id(id):
        """
        Get a chat message by id.

        Will raise `werkzeug.errors.NotFound`
        exception if SQLAlchemy cannot find the
        message with the provided ID.

        param `id` type Integer
        """
        message = ChatMessage.query.filter(ChatMessage.id == id).first()
        if message is None:
            raise NotFound(response={
                "message": "A message was not found with the provided id."
            })
        return message

    # Instance methods
    def user_by_id_is_sender(self, user_id):
        """
        Check if the user id provided is the
        user id of the sender.

        Will raise `werkzeug.errors.Forbidden`
        exception if the provided id is not the
        requestor id.

        param `user_id` type Integer
        """
        if user_id != self.sender_user_id:
            raise Forbidden(response={
                "message": "User is not the sender of this message."
            })

    # Scopes
    def to_json(self):
        return {
            "id": self.id,
            "userConnectionId": self.user_connection_id,
            "senderUserId": self.sender_user_id,
            "senderUserFirstName": self.sender.first_name,
            "senderUserLastName": self.sender.last_name,
            "body": self.body,
        }
