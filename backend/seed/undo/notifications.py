from models import db


def down():
    db.session.execute('DELETE FROM notifications;')
    db.session.execute('ALTER SEQUENCE notifications_id_seq RESTART WITH 1;')
    db.session.commit()
