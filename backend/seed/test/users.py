from models import db, Email, Password, User

PASSWORD = "Password1234$"

seed = [
    # Cluster 1
    {
        "init": {
            "first_name": "UserA",
            "last_name": "UserA",
        },
        "email": "A@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "UserB",
            "last_name": "UserB",
        },
        "email": "B@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "UserC",
            "last_name": "UserC",
        },
        "email": "C@email.com",
        "password": PASSWORD,
    },

    # Cluster 2
    {
        "init": {
            "first_name": "UserD",
            "last_name": "UserD",
        },
        "email": "D@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "UserE",
            "last_name": "UserE",
        },
        "email": "E@email.com",
        "password": PASSWORD,
    },
]


def up():
    for item in seed:
        user = User(**item["init"])

        db.session.add(user)
        db.session.commit()

        user.set_active_email_address(item["email"])
        user.set_active_password(item["password"])
    
    db.session.commit()
