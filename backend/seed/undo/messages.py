from models import db


def down():
    db.session.execute('DELETE FROM messages;')
    db.session.execute('ALTER SEQUENCE messages_id_seq RESTART WITH 1;')
    db.session.commit()
