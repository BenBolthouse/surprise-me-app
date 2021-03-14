

from models import db, ChatMessage


seed = [
    (6, 1, 35, "Hey, welcome!", "2021-02-05T12:12:00:000Z"),
    (6, 35, 1, "Thanks! How's it going?", "2021-02-05T12:13:01:000Z"),
    (6, 1, 35, "Another day another dollar", "2021-02-05T12:13:11:000Z"),
    (6, 1, 35, "Are you gonna send me a gift??", "2021-02-05T12:13:26:000Z"),
    (6, 35, 1, "Well I just got here! Patience...", "2021-02-05T12:13:55:000Z"),
]


def seed_chat_messages():
    for item in seed:
        x = ChatMessage({
            "user_connection_id": item[0],
            "sender_user_id": item[1],
            "recipient_user_id": item[2],
            "body": item[3],
        })
        x.established_at = item[4]
        db.session.add(x)
        db.session.commit()


def seed_undo_chat_messages():
    db.session.execute('DELETE FROM chat_messages;')
    db.session.execute('ALTER SEQUENCE chat_messages_id_seq RESTART WITH 1;')
    db.session.commit()
