from flask_socketio import emit, send


from app import socketio


# Sends a notification to a user via a user's room id.
def send_notification(payload, recipient_id):
    raise Exception("Not implemented")
