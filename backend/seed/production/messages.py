from datetime import datetime


from models import db, Connection, Message


seed = [
    # Cluster 2
    {
        "init": {
            "connection_id": 9,
            "sender_id": 16,
            "recipient_id": 5,
            "body": "Albatross",
        },
        "created_at_minutes": "01",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 9,
            "recipient_id": 4,
            "body": "Bolivia",
        },
        "created_at_minutes": "02",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 16,
            "recipient_id": 5,
            "body": "Carpenter",
        },
        "created_at_minutes": "03",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 9,
            "recipient_id": 4,
            "body": "Dungeon",
        },
        "created_at_minutes": "04",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 16,
            "recipient_id": 5,
            "body": "Epicenter",
        },
        "created_at_minutes": "05",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 9,
            "recipient_id": 4,
            "body": "Foundation",
        },
        "created_at_minutes": "06",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 16,
            "recipient_id": 5,
            "body": "Gargoyle",
        },
        "created_at_minutes": "07",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 9,
            "recipient_id": 4,
            "body": "Helper",
        },
        "created_at_minutes": "08",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 16,
            "recipient_id": 5,
            "body": "Indigo",
        },
        "created_at_minutes": "09",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 9,
            "recipient_id": 4,
            "body": "Jasmine",
        },
        "created_at_minutes": "11",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 16,
            "recipient_id": 5,
            "body": "Kite",
        },
        "created_at_minutes": "12",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 9,
            "recipient_id": 4,
            "body": "Lemon",
        },
        "created_at_minutes": "13",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 16,
            "recipient_id": 5,
            "body": "Marriage",
        },
        "created_at_minutes": "14",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 9,
            "recipient_id": 4,
            "body": "Nunchuck",
        },
        "created_at_minutes": "15",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 16,
            "recipient_id": 5,
            "body": "Opera",
        },
        "created_at_minutes": "16",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 9,
            "recipient_id": 4,
            "body": "Potatoskin",
        },
        "created_at_minutes": "17",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 16,
            "recipient_id": 5,
            "body": "Quintet",
        },
        "created_at_minutes": "18",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 9,
            "recipient_id": 4,
            "body": "Risotto",
        },
        "created_at_minutes": "19",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 16,
            "recipient_id": 5,
            "body": "Shoulder",
        },
        "created_at_minutes": "20",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 9,
            "recipient_id": 4,
            "body": "Tapioca",
        },
        "created_at_minutes": "21",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 16,
            "recipient_id": 5,
            "body": "Underway",
        },
        "created_at_minutes": "22",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 9,
            "recipient_id": 4,
            "body": "Visceral",
        },
        "created_at_minutes": "23",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 16,
            "recipient_id": 5,
            "body": "Wowza",
        },
        "created_at_minutes": "24",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 9,
            "recipient_id": 4,
            "body": "Xray",
        },
        "created_at_minutes": "25",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 16,
            "recipient_id": 5,
            "body": "Yellow",
        },
        "created_at_minutes": "26",
    },
    {
        "init": {
            "connection_id": 9,
            "sender_id": 9,
            "recipient_id": 4,
            "body": "Zipper",
        },
        "created_at_minutes": "28",
    }
]


def up():
    for item in seed:
        message = Message(**item["init"])

        minutes = item["created_at_minutes"]
        message.created_at = datetime.fromisoformat(f"2021-10-10T12:{minutes}:00.000000")

        db.session.add(message)

    db.session.commit()
