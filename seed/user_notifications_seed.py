# cSpell:disable

from datetime import datetime


from models import db, UserNotification


seed = [
    (1, "USER_CONN_REQ", "http://localhost:5000/api/connections/1", "Sydney Youngman sent you a friend request."),
    (1, "USER_CONN_REQ", "http://localhost:5000/api/connections/2", "Tandie Garling sent you a friend request."),
    (1, "USER_CONN_REQ", "http://localhost:5000/api/connections/3", "Anjanette Nehl sent you a friend request."),
]


def seed_user_notifications():
    for item in seed:
        x = UserNotification({
            "user_id": item[0],
            "notification_type": item[1],
            "hook": item[2],
            "body": item[3],
        })
        db.session.add(x)
        db.session.commit()


def seed_undo_user_notifications():
    db.session.execute('DELETE FROM user_notifications;')
    db.session.execute('ALTER SEQUENCE user_notifications_id_seq RESTART WITH 1;')
    db.session.commit()
