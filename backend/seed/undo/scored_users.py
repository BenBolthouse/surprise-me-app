from models import db


def down():
    db.session.execute('DELETE FROM scored_users;')
    db.session.execute('ALTER SEQUENCE scored_users_id_seq RESTART WITH 1;')
    db.session.commit()
