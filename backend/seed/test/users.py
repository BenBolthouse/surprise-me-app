from models import db, Email, Password, User


seed = [
    {
        "first_name": "UserA",
        "last_name": "UserA",
        "email": "A@email.com",
        "password": "Password1234$",
    },
    {
        "first_name": "UserB",
        "last_name": "UserB",
        "email": "B@email.com",
        "password": "Password1234$",
    },
    {
        "first_name": "UserC",
        "last_name": "UserC",
        "email": "C@email.com",
        "password": "Password1234$",
    },
    {
        "first_name": "UserD",
        "last_name": "UserD",
        "email": "D@email.com",
        "password": "Password1234$",
    },
]


def up():
    for item in seed:
        user = User(**item)

        db.session.add(user)
        db.session.commit()

        user.set_active_email_address(item["email"])
        user.set_active_password(item["password"])

        db.session.commit()
