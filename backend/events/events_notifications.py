from flask import Blueprint
from flask_socketio import emit, send


from app import socketio
from models import db


notification_events = Blueprint("notification_events", __name__)


# Sends a notification to a user via a user's room id and then persists the
# notification to the data store.
def send_notification(payload, notification):
    # TODO add websocket emit for notification channel

    db.session.add(notification)
    db.session.commit()

    return True
