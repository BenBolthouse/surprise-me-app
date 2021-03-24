# cSpell:disable

from datetime import datetime


from models import db, UserConnection


seed = [
    (30, 1, None),  # ----------- 1
    (31, 1, None),  # ----------- 2
    (32, 1, None),  # ----------- 3
    (33, 1, datetime.now()),  # - 4
    (34, 1, datetime.now()),  # - 5
    (35, 1, datetime.now()),  # - 6
    (1, 2, None),  # ------------ 7
    (1, 3, None),  # ------------ 8
    (1, 4, datetime.now()),  # -- 9
    (1, 5, datetime.now()),  # -- 10
    (1, 6, datetime.now()),  # -- 11
    (1, 7, datetime.now()),  # -- 12
    (1, 8, datetime.now()),  # -- 13
    (1, 9, datetime.now()),  # -- 14
    (1, 10, datetime.now()),  # - 15
    (1, 12, None),  # ----------- 16
    (1, 13, None),  # ----------- 17
    (1, 14, datetime.now()),  # - 18
    (1, 15, datetime.now()),  # - 19
    (1, 16, datetime.now()),  # - 20
    (1, 17, None),  # ----------- 21
    (1, 18, datetime.now()),  # - 22
    (1, 19, datetime.now()),  # - 23
    (1, 20, datetime.now()),  # - 24
    (1, 22, None),  # ----------- 25
    (1, 23, None),  # ----------- 26
    (1, 24, datetime.now()),  # - 27
    (1, 25, None),  # ----------- 28
    (1, 26, datetime.now()),  # - 29
    (1, 27, datetime.now()),  # - 30
    (1, 28, None),  # ----------- 31
    (1, 29, None),  # ----------- 32
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
