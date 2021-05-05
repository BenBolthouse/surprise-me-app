from models import db, Email, Password, User

PASSWORD = "Password1234$"

seed = [
    {
        "init": {
            "first_name": "Kristi",
            "last_name": "Reblon",
        },
        "email": "k.reblon@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Angela",
            "last_name": "Furrier",
        },
        "email": "a.furrier@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Andrea",
            "last_name": "LeBlanc",
        },
        "email": "a.leblanc@email.com",
        "password": PASSWORD,
    },

    {
        "init": {
            "first_name": "Phil",
            "last_name": "Piacqu",
        },
        "email": "p.piacqu@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Ahmed",
            "last_name": "Kalhma",
        },
        "email": "a.kalhma@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "John-Michael",
            "last_name": "Longmoor",
        },
        "email": "j.longmoor@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Andy",
            "last_name": "Zimmerman",
        },
        "email": "a.zimmerman@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Lane",
            "last_name": "Barnett",
        },
        "email": "l.barnett@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Jack",
            "last_name": "Braavos",
        },
        "email": "j.braavos@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Dennis",
            "last_name": "Anderson",
        },
        "email": "d.anderson@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Javin",
            "last_name": "Holdbrook",
        },
        "email": "j.holdbrook@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Lloyd",
            "last_name": "Yans",
        },
        "email": "l.yans@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Martin",
            "last_name": "Targaryen",
        },
        "email": "m.targaryen@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Sarah",
            "last_name": "Helper",
        },
        "email": "s.helper@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Emily",
            "last_name": "Harper",
        },
        "email": "e.harper@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Steve",
            "last_name": "Primrose",
        },
        "email": "s.primrose@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Eddy",
            "last_name": "June",
        },
        "email": "e.june@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Marcus",
            "last_name": "Stark",
        },
        "email": "m.stark@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Vincent",
            "last_name": "Jazzhands",
        },
        "email": "v.jazzhands@email.com",
        "password": PASSWORD,
    },
    {
        "init": {
            "first_name": "Summer",
            "last_name": "Chen",
        },
        "email": "s.chen@email.com",
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
