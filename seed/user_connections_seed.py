# cSpell:disable

from datetime import datetime


from models import db, UserConnection


seed = [
    (30, 1, None),
    (31, 1, None),
    (32, 1, None),
    (1, 2, None),
    (1, 3, None),
    (1, 4, datetime.now()),
    (1, 5, datetime.now()),
    (1, 6, datetime.now()),
    (1, 7, datetime.now()),
    (1, 8, datetime.now()),
    (1, 9, datetime.now()),
    (1, 10, datetime.now()),
    (1, 12, None),
    (1, 13, None),
    (1, 14, datetime.now()),
    (1, 15, datetime.now()),
    (1, 16, datetime.now()),
    (1, 17, None),
    (1, 18, datetime.now()),
    (1, 19, datetime.now()),
    (1, 20, datetime.now()),
    (1, 22, None),
    (1, 23, None),
    (1, 24, datetime.now()),
    (1, 25, None),
    (1, 26, datetime.now()),
    (1, 27, datetime.now()),
    (1, 28, None),
    (1, 29, None),
]


def seed_user_connections():
    for item in seed:
        x = UserConnection({
            "requestor_user_id": item[0],
            "recipient_user_id": item[1],
        })
        x.established_at = item[2]
        db.session.add(x)
        db.session.commit()


def seed_undo_user_connections():
    db.session.execute('DELETE FROM user_connections;')
    db.session.execute('ALTER SEQUENCE user_connections_id_seq RESTART WITH 1;')
    db.session.commit()
