from models import db, Connection


seed = [
    # Cluster 1
    {
        # UserB --> UserA
        "init": {
            "requestor_id": 2,
            "approver_id": 1,
        },
        "approve": True,
    },
    {
        # UserB --> UserC
        "init": {
            "requestor_id": 2,
            "approver_id": 3,
        },
        "approve": False,
    },

    # Cluster 2
    {
        # UserD --> UserE
        "init": {
            "requestor_id": 4,
            "approver_id": 5,
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
