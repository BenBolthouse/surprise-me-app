from models import db, Notification


seed = [
    {
        "init": {
            "type": "CONNECTION",
            "recipient_id": 16,
            "body": "This is a notification body",
            "action": "https://www.google.com/",
        },
        "approve": False,
    },
    {
        "init": {
            "type": "CONNECTION",
            "recipient_id": 16,
            "body": "This is a notification body",
            "action": "https://www.google.com/",
        },
        "approve": False,
    },
    {
        "init": {
            "type": "CONNECTION",
            "recipient_id": 16,
            "body": "This is a notification body",
            "action": "https://www.google.com/",
        },
        "approve": False,
    },
    {
        "init": {
            "type": "CONNECTION",
            "recipient_id": 16,
            "body": "This is a notification body",
            "action": "https://www.google.com/",
        },
        "approve": False,
    },
    {
        "init": {
            "type": "CONNECTION",
            "recipient_id": 16,
            "body": "This is a notification body",
            "action": "https://www.google.com/",
        },
        "approve": False,
    },
    {
        "init": {
            "type": "CONNECTION",
            "recipient_id": 16,
            "body": "This is a notification body",
            "action": "https://www.google.com/",
        },
        "approve": False,
    },
    {
        "init": {
            "type": "CONNECTION",
            "recipient_id": 16,
            "body": "This is a notification body",
            "action": "https://www.google.com/",
        },
        "approve": False,
    },
    {
        "init": {
            "type": "CONNECTION",
            "recipient_id": 16,
            "body": "This is a notification body",
            "action": "https://www.google.com/",
        },
        "approve": False,
    },
    {
        "init": {
            "type": "CONNECTION",
            "recipient_id": 16,
            "body": "This is a notification body",
            "action": "https://www.google.com/",
        },
        "approve": False,
    },
    {
        "init": {
            "type": "CONNECTION",
            "recipient_id": 16,
            "body": "This is a notification body",
            "action": "https://www.google.com/",
        },
        "approve": False,
    },
]


def up():
    for item in seed:
        notification = Notification(**item["init"])

        db.session.add(notification)

    db.session.commit()
