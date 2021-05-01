from models import db, Connection


seed = [
    {
        # UserB --> UserA
        "init": {
            "requestor_id": 2,
            "recipient_id": 1,
        },
        "approve": True,
    },
    {
        # UserB --> UserC
        "init": {
            "requestor_id": 2,
            "recipient_id": 3,
        },
        "approve": False,
    },
]


def up():
    for item in seed:
        connection = Connection(**item["init"])

        if item["approve"]:
            connection.approve()

        db.session.add(connection)
        db.session.commit()
