from werkzeug.exceptions import NotFound, BadRequest, Forbidden


from .db import db


class ChatMessage(db.Model):
    def __init__(self, config_object):
        self.user_connection_id = config_object["user_connection_id"]
        self.sender_user_id = config_object["sender_user_id"]
        self.recipient_user_id = config_object["recipient_user_id"]
        self.body = config_object["body"]

    # ** «««««««««««««««« Mapped Properties »»»»»»»»»»»»»»»» **

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
    recipient_user_id = db.Column(
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

    # ** «««««««««««««««« Scopes »»»»»»»»»»»»»»»» **

    def to_json(self):
        return {
            "id": self.id,
            "userConnectionId": self.user_connection_id,
            "sender": self.sender.to_json_without_coordinates(),
            "body": self.body if not self.deleted else None,
            "deleted": self.deleted,
            "updated": self.updated,
            "createdAt": self.created_at,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "user_connection_id": self.user_connection_id,
            "sender": self.sender.to_dict(),
            "recipient_user_id": self.recipient_user_id,
            "body": self.body,
            "deleted": self.deleted,
            "updated": self.updated,
            "created_at": self.created_at,
        }

    # ** «««««««««««««««« Associations »»»»»»»»»»»»»»»» **

    _sender_user = db.relationship(
        "User",
        back_populates="_chat_messages",
        foreign_keys=[sender_user_id])

    # ** «««««««««««««««« Getters and Setters »»»»»»»»»»»»»»»» **

    # «««««««« Sender User »»»»»»»»

    @property
    def sender(self):
        return self._sender_user

    # ** «««««««««««««««« Static Class Methods »»»»»»»»»»»»»»»» **

    @staticmethod
    def exists(id):
        message = ChatMessage.query.get(id)
        if message is None:
            raise NotFound(response={
                "message": "A message was not found with the provided id."
            })
        return message

    @staticmethod
    def require_body_text(body):
        if body == "" or body is None:
            raise BadRequest(response={
                "message": "The message body cannot be empty or null."
            })
        return True

    # ** «««««««««««««««« Instance Methods »»»»»»»»»»»»»»»» **

    def user_is_sender(self, user_id):
        if user_id != self.sender_user_id:
            raise Forbidden(response={
                "message": "User is not the sender of this message."
            })
        return True
