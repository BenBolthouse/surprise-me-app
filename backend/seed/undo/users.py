from models import db


def down():
    db.session.execute('DELETE FROM users;')
    db.session.execute('ALTER SEQUENCE users_id_seq RESTART WITH 1;')
