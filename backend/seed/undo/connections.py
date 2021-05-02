from models import db


def down():
    db.session.execute('DELETE FROM connections;')
    db.session.execute('ALTER SEQUENCE connections_id_seq RESTART WITH 1;')
