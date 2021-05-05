from models import db, Connection


seed = [
    # Cluster 1
    {
        # UserB --> UserA
        "init": {
            "requestor_id": 16,
            "approver_id": 1,
        },
        "approve": False,
    },
    {
        # UserB --> UserC
        "init": {
            "requestor_id": 16,
            "approver_id": 2,
        },
        "approve": False,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 16,
            "approver_id": 3,
        },
        "approve": False,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 16,
            "approver_id": 4,
        },
        "approve": False,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 5,
            "approver_id": 16,
        },
        "approve": False,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 6,
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
            "requestor_id": 16,
            "approver_id": 9,
        },
        "approve": True,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 16,
            "approver_id": 10,
        },
        "approve": True,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 16,
            "approver_id": 12,
        },
        "approve": True,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 16,
            "approver_id": 13,
        },
        "approve": True,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 17,
            "approver_id": 16,
        },
        "approve": True,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 18,
            "approver_id": 16,
        },
        "approve": True,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 19,
            "approver_id": 16,
        },
        "approve": True,
    },
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 20,
            "approver_id": 16,
        },
        "approve": True,
    },
]


def up():
    for item in seed:
        connection = Connection(**item["init"])

        if item["approve"]:
            connection.approve()

        db.session.add(connection)

    db.session.commit()
