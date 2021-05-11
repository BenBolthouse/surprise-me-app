from models import db, Product


seed = [
    {
        "init": {
            "name": "Black Utility Keychain",
            "description": "For all your keychain needs! Makes a Swiss Army knife look like a child's toy.",
            "price": 42.95,
            "latitude": 32.28181897780636,
            "longitude": -111.0231027868138,
        },
    },
    {
        "init": {
            "name": "Desk Lamp Industrial",
            "description": "Sleek and sophisticated. Your future will be bright, we know it.",
            "price": 59.99,
            "latitude": 32.36037708508069,
            "longitude": -111.08719393142202,
        },
    },
    {
        "init": {
            "name": "Black Utility Keychain",
            "description": "For all your keychain needs! Makes a Swiss Army knife look like a child's toy.",
            "price": 42.95,
            "latitude": 32.17338494132557,
            "longitude": -110.93764792733616,
        },
    },
    {
        "init": {
            "name": "Desk Lamp Industrial",
            "description": "Sleek and sophisticated. Your future will be bright, we know it.",
            "price": 59.99,
            "latitude": 32.23006030610265,
            "longitude": -110.97864316397745,
        },
    },
    {
        "init": {
            "name": "Black Utility Keychain",
            "description": "For all your keychain needs! Makes a Swiss Army knife look like a child's toy.",
            "price": 42.95,
            "latitude": 32.42522148288474,
            "longitude": -110.96132123300225,
        },
    },
    {
        "init": {
            "name": "Desk Lamp Industrial",
            "description": "Sleek and sophisticated. Your future will be bright, we know it.",
            "price": 59.99,
            "latitude": 32.28084267225804,
            "longitude": -110.9647856191973,
        },
    },
    {
        "init": {
            "name": "Black Utility Keychain",
            "description": "For all your keychain needs! Makes a Swiss Army knife look like a child's toy.",
            "price": 42.95,
            "latitude": 32.42083498508482,
            "longitude": -110.7574998451941,
        },
    },
]


def up():
    for item in seed:
        product = Product(**item["init"])

        db.session.add(product)

    db.session.commit()
