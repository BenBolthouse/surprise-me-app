from datetime import datetime


from models import db, ChatMessage


seed = [

    # Charlena Meanwell (1) && Inigo Dur (35)
    (6, 35, 1, "Hey what's up", "2021-01-05", "13", "12", "05"),
    (6, 1, 35, "Not much! How's life?", "2021-01-05", "13", "12", "24"),
    (6, 1, 35, "How's the new place?", "2021-01-05", "13", "12", "27"),
    (6, 35, 1, "Pretty cool", "2021-01-05", "13", "14", "01"),
    (6, 35, 1, "Getting accustomed to the new city", "2021-01-05", "13", "14", "12"),
    (6, 1, 35, "Oh yeah I heard you moved hows SF", "2021-01-05", "13", "15", "22"),
    (6, 1, 35, "Not too bad lots to see", "2021-01-05", "13", "15", "22"),

    # Charlena Meanwell (1) && Galvin Bogace (4)
    (9, 4, 1, "Hey what's up", "2021-01-05", "13", "12", "05"),
    (9, 1, 4, "Not much! How's life?", "2021-01-05", "13", "12", "24"),
    (9, 1, 4, "How's the new place?", "2021-01-05", "13", "12", "27"),
    (9, 4, 1, "Pretty cool", "2021-01-05", "13", "14", "01"),
    (9, 4, 1, "Getting accustomed to the new city", "2021-01-05", "13", "14", "12"),
    (9, 1, 4, "Oh yeah I heard you moved hows SF", "2021-01-05", "13", "15", "22"),
    (9, 1, 4, "Not too bad lots to see", "2021-01-05", "13", "15", "22"),

    # Charlena Meanwell (1) && Bryna Sainte Paul (5)
    (10, 5, 1, "Hey what's up", "2021-01-05", "13", "12", "05"),
    (10, 1, 5, "Not much! How's life?", "2021-01-05", "13", "12", "24"),
    (10, 1, 5, "How's the new place?", "2021-01-05", "13", "12", "27"),
    (10, 5, 1, "Pretty cool", "2021-01-05", "13", "14", "01"),
    (10, 5, 1, "Getting accustomed to the new city", "2021-01-05", "13", "14", "12"),
    (10, 1, 5, "Oh yeah I heard you moved hows SF", "2021-01-05", "13", "15", "22"),
    (10, 1, 5, "Not too bad lots to see", "2021-01-05", "13", "15", "22"),

    # Charlena Meanwell (1) && Alanson Monnoyer (6)
    (11, 6, 1, "Hey what's up", "2021-01-05", "13", "12", "05"),
    (11, 1, 6, "Not much! How's life?", "2021-01-05", "13", "12", "24"),
    (11, 1, 6, "How's the new place?", "2021-01-05", "13", "12", "27"),
    (11, 6, 1, "Pretty cool", "2021-01-05", "13", "14", "01"),
    (11, 6, 1, "Getting accustomed to the new city", "2021-01-05", "13", "14", "12"),
    (11, 1, 6, "Oh yeah I heard you moved hows SF", "2021-01-05", "13", "15", "22"),
    (11, 1, 6, "Not too bad lots to see", "2021-01-05", "13", "15", "22"),

    # Charlena Meanwell (1) && Etti Restill (7)
    (12, 7, 1, "Hey what's up", "2021-01-05", "13", "12", "05"),
    (12, 1, 7, "Not much! How's life?", "2021-01-05", "13", "12", "24"),
    (12, 1, 7, "How's the new place?", "2021-01-05", "13", "12", "27"),
    (12, 7, 1, "Pretty cool", "2021-01-05", "13", "14", "01"),
    (12, 7, 1, "Getting accustomed to the new city", "2021-01-05", "13", "14", "12"),
    (12, 1, 7, "Oh yeah I heard you moved hows SF", "2021-01-05", "13", "15", "22"),
    (12, 1, 7, "Not too bad lots to see", "2021-01-05", "13", "15", "22"),

    # Charlena Meanwell (1) && Xena Greguoli (8)
    (13, 8, 1, "Hey what's up", "2021-01-05", "13", "12", "05"),
    (13, 1, 8, "Not much! How's life?", "2021-01-05", "13", "12", "24"),
    (13, 1, 8, "How's the new place?", "2021-01-05", "13", "12", "28"),
    (13, 8, 1, "Pretty cool", "2021-01-05", "13", "14", "01"),
    (13, 8, 1, "Getting accustomed to the new city", "2021-01-05", "13", "14", "12"),
    (13, 1, 8, "Oh yeah I heard you moved hows SF", "2021-01-05", "13", "15", "22"),
    (13, 1, 8, "Not too bad lots to see", "2021-01-05", "13", "15", "22"),

    # Charlena Meanwell (1) && Rebecca Romain (8)
    (14, 9, 1, "Hey what's up", "2021-01-05", "13", "12", "05"),
    (14, 1, 9, "Not much! How's life?", "2021-01-05", "13", "12", "24"),
    (14, 1, 9, "How's the new place?", "2021-01-05", "13", "12", "29"),
    (14, 9, 1, "Pretty cool", "2021-01-05", "13", "14", "01"),
    (14, 9, 1, "Getting accustomed to the new city", "2021-01-05", "13", "14", "12"),
    (14, 1, 9, "Oh yeah I heard you moved hows SF", "2021-01-05", "13", "15", "22"),
    (14, 1, 9, "Not too bad lots to see", "2021-01-05", "13", "15", "22"),

]


def seed_chat_messages():
    for item in seed:
        x = ChatMessage({
            "user_connection_id": item[0],
            "sender_user_id": item[1],
            "recipient_user_id": item[2],
            "body": item[3],
        })
        time = f"{item[4]}T{item[5]}:{item[6]}:{item[7]}.000Z"
        x.created_at = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        db.session.add(x)
        db.session.commit()


def seed_undo_chat_messages():
    db.session.execute('DELETE FROM chat_messages;')
    db.session.execute('ALTER SEQUENCE chat_messages_id_seq RESTART WITH 1;')
    db.session.commit()
