from datetime import datetime


from .db import db


class Notification(db.Model):
    __tablename__ = "notifications"

    # Mapping -----------------------------------
    id = db.Column(
        db.Integer,
        primary_key=True)
    connection = db.Column(
        db.Integer,
        db.ForeignKey('connections.id'),
        nullable=False)
    sender = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    recipient = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    type = db.Column(
        db.String(64),
        nullable=False)
    _body = db.Column(
        db.String(),
        name="body",
        nullable=False,
        default="")
    action = db.Column(
        db.String(255),
        nullable=True,
        default=None)
    _visibility = db.Column(
        db.Boolean,
        nullable=False,
        default=True)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    seen_at = db.Column(
        db.DateTime,
        name="seen_at",
        nullable=True,
        default=None)
    updated_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)
    deleted_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)

    # Properties --------------------------------
    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value
        self.updated_at = datetime.now()

    @property
    def visibility(self):
        return self._visibility

    @visibility.setter
    def visibility(self, value):
        self._visibility = value
        self.updated_at = datetime.now() if value is True else self.updated_at

    # Constructor -------------------------------
    def __init__(self):
        # Creating instances of Message class is disallowed; the dev
        # should select from one of Message class' children classes.
        # This is a strongly enforced rule preventing incorrect pseudo
        # types of the Message class from being persisted to the data
        # store.
        raise Exception(
            "Message is a parent class and cannot be instantiated. Use a child class of Message to create a message object.")


class ChatMessage(Message):
    def __init__(self, connection, sender_id, body):
        self.connection = connection.id
        self.sender = sender_id
        self.recipient = connection.other_user(sender_id).id
        self.type = "CHAT_TEXT"
        self.body = body


class ChatReactionMessage(Message):
    def __init__(self, connection, sender_id, reaction):
        self.connection = connection.id
        self.sender = sender_id
        self.recipient = connection.other_user(sender_id).id
        self.type = "CHAT_REACTION"
        self.body = (reaction if reaction in self.reactions
                     else raise Exception("Reaction is not a valid reaction."))

    # List of all valid chat reactions.
    # Any invalid reaction with raise an exception.
    reactions = {
        "smile",
        "like",
        "frown",
        "sad",
    }


class ChatGiftMessage(Message):
    def __init__(self, connection, sender_id, reaction):
        self.connection = connection.id
        self.sender = sender_id
        self.recipient = connection.other_user(sender_id).id
        self.type = "CHAT_GIFT"
        self.action = f"{PUBLIC_URL}/connections/{connection.id}/gifts/{purchase_id}"
        self.visibility = False
