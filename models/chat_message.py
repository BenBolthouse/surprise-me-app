from werkzeug.exceptions import NotFound, BadRequest


from .db import db


class ChatMessage(db.Model):
    def __init__(self, sender_user_id, body):
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

        Will raise `werkzeug.errors.BadRequest`
        exception if the provided id is not the
        requestor id.

        param `user_id` type Integer
        """
        if user_id != self.sender_user_id:
            raise BadRequest(response={
                "message": "User is not the sender of this message."
            })

    # Scopes
    def to_json_on_create(self):
        return {
            "id": self.id,
            "userConnectionId": self.user_connection_id,
            "senderUserId": self.sender_user_id,
            "body": self.body,
            "createdAt": self.created_at,
        }

    def to_json_on_get(self):
        return {
            "id": self.id,
            "userConnectionId": self.user_connection_id,
            "senderUserId": self.sender_user_id,
            "body": self.body,
            "updated": self.updated,
            "createdAt": self.created_at,
        }

    def to_json_on_patch(self):
        return {
            "id": self.id,
            "userConnectionId": self.user_connection_id,
            "senderUserId": self.sender_user_id,
            "body": self.body,
            "updated": self.updated,
            "createdAt": self.created_at,
        }
