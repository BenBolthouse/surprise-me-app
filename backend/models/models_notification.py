from datetime import datetime


from .db import db


class Notification(db.Model):
    __tablename__ = "notifications"

    # Mapping -----------------------------------
    id = db.Column(
        db.Integer,
        primary_key=True)
    user = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    type = db.Column(
        db.String(64),
        nullable=False)
    title = db.Column(
        db.String(64),
        nullable=False,
        default="")
    body = db.Column(
        db.String(255),
        nullable=False,
        default="")
    action = db.Column(
        db.String(255),
        nullable=False,
        default="")
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now())
    _seen_at = db.Column(
        db.DateTime,
        name="seen_at",
        nullable=True,
        default=None)
    _dismissed_at = db.Column(
        db.DateTime,
        name="dismissed_at",
        nullable=True,
        default=None)

    # Properties --------------------------------
    @property
    def seen_at(self):
        return self._seen_at

    @seen_at.setter
    def seen_at(self):
        self._seen_at = datetime.now()

    @property
    def dismissed_at(self):
        return self._dismissed_at

    @dismissed_at.setter
    def dismissed_at(self):
        timestamp = datetime.now()
        if self._seen_at is not None:
            self._seen_at = timestamp
        self._dismissed_at = timestamp

    # Constructor -------------------------------
    def __init__(self):
        # Creating instances of Notification class is disallowed; the dev should
        # select from one of Notification class' children classes. This is a
        # strongly enforced rule preventing incorrect pseudo types of the
        # Notification class from being persisted to the data store.
        raise Exception("Notification is a parent class and cannot be instantiated. Use a child class of Notification to create a notification object.")


class MessageNotification(Notification):
    def __init__(self, recipient_id, connection_id, sender_user):
        self.user = recipient_id
        self.type = "MESSAGE"
        self.title = f"{sender_user.first_name} {sender_user.last_name} sent you a message"
        self.action = f"{PUBLIC_URL}/messages/{connection_id}"


class GiftNotification(Notification):
    def __init__(self, recipient_id, purchase_id, sender_user):
        self.user = recipient_id
        self.type = "GIFT"
        self.title = f"{sender_user.first_name} {sender_user.last_name} sent you a gift"
        self.action = f"{PUBLIC_URL}/gifts/{purchase_id}"


class AppNotification(Notification):
    def __init__(self, recipient_id, title, body, action):
        self.user = recipient_id
        self.type = "APP"
        self.title = title
        self.body = body
        self.action = PUBLIC_URL + action
