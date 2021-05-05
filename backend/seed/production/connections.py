from models import db, Connection


seed = [
    # Cluster 1
    {
        # UserB --> UserA
        "init": {
            "requestor_id": 16,
            "approver_id": 4,
        },
        "approve": False,
    },
    {
        # UserB --> UserC
        "init": {
            "requestor_id": 16,
            "approver_id": 5,
        },
        "approve": False,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 16,
            "approver_id": 6,
        },
        "approve": False,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 3,
            "approver_id": 16,
        },
        "approve": False,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 7,
            "approver_id": 16,
        },
        "approve": False,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 8,
            "approver_id": 16,
        },
        "approve": False,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 9,
            "approver_id": 16,
        },
        "approve": False,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 10,
            "approver_id": 16,
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
