from datetime import datetime
import json
import pytest
import os


from app import app
from models import db, User, UserConnection, ChatMessage


@pytest.fixture(scope="function")
def client():
    """
    Establishes a client context for sending
    requests to the API. Teardown removes
    all records from all database tables and
    resets primary key sequences to 1.
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"].replace("surprise_me_dev", "surprise_me_test")
    with app.test_client() as client:
        with app.app_context():
            yield client
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                print('Clear table %s' % table)
                db.engine.execute(table.delete())
                db.engine.execute("ALTER SEQUENCE %s_id_seq RESTART WITH 1;" % table)  # noqa
            db.session.commit()


@pytest.fixture(scope="function")
def headers(client):
    """
    Requests an anti-csrf token from the API
    and returns a header object for client
    POST, PATCH and DELETE requests.
    """
    response = client.get("/api/csrf")
    yield {
        "Content-Type": "application/json",
        "Allow": "application/json",
        "X-CSRFToken": response.json.get("data")["token"]
    }


@pytest.fixture(scope="function", autouse=True)
def database_seed_demo_users(client, headers):
    """
    Creates a series of demo users in the
    database.
    """
    user_templates = [
        {
            "password": "Password1234$",
            "first_name": "Angelica",
            "last_name": "Ashworthy",
            "email": "database_user_a@example.com",
            "share_location": True,
            "coord_lat": 123.123456,
            "coord_long": 12.123456,
        },
        {
            "password": "Password1234$",
            "first_name": "Benny",
            "last_name": "Broomtaker",
            "email": "database_user_b@example.com",
            "share_location": True,
            "coord_lat": 123.123456,
            "coord_long": 12.123456,
        },
        {
            "password": "Password1234$",
            "first_name": "Charlie",
            "last_name": "Caninetooth",
            "email": "database_user_c@example.com",
            "share_location": True,
            "coord_lat": 123.123456,
            "coord_long": 12.123456,
        },
        {
            "password": "Password1234$",
            "first_name": "Denise",
            "last_name": "Dogood",
            "email": "database_user_d@example.com",
            "share_location": True,
            "coord_lat": 123.123456,
            "coord_long": 12.123456,
        },
        {
            "password": "Password1234$",
            "first_name": "Emily",
            "last_name": "Earwhisper",
            "email": "database_user_e@example.com",
            "share_location": True,
            "coord_lat": 123.123456,
            "coord_long": 12.123456,
        },
        {
            "password": "Password1234$",
            "first_name": "Frank",
            "last_name": "Farquad",
            "email": "database_user_f@example.com",
            "share_location": True,
            "coord_lat": 123.123456,
            "coord_long": 12.123456,
        },
        {
            "password": "Password1234$",
            "first_name": "Gregory",
            "last_name": "Gearhead",
            "email": "database_user_g@example.com",
            "share_location": True,
            "coord_lat": 123.123456,
            "coord_long": 12.123456,
        },
        {
            "password": "Password1234$",
            "first_name": "Harriet",
            "last_name": "Halibut",
            "email": "database_user_h@example.com",
            "share_location": True,
            "coord_lat": 123.123456,
            "coord_long": 12.123456,
        },
    ]

    for user_template in user_templates:
        user = User(user_template)
        db.session.add(user)
    db.session.commit()

    # Yield users data for testing purposes
    yield user_templates


@pytest.fixture(scope="function")
def database_seed_demo_connections_from_user_a(
        client, headers, database_seed_demo_users):
    """
    Creates a series of connections between demo users.
    """
    connection_templates = [2, 3, 4, 5, 6, 7]

    for connection_template in connection_templates:
        conn = UserConnection({
            "requestor_user_id": 1,
            "recipient_user_id": connection_template,
        })

        if connection_template > 4:
            conn.established_at = datetime.now()

        db.session.add(conn)
    db.session.commit()

    # Yield users data for testing purposes
    yield connection_templates


@pytest.fixture(scope="function")
def database_seed_demo_message_user_a_and_b(
        client, headers, database_seed_demo_users,
        database_seed_demo_connections_from_user_a):
    """
    Creates a series of messages between demo users A and B.
    """
    message_templates = [
        (1, 5, "Hola", "2020-11-27T12:00:10.000000"),
        (5, 1, "Como estas?", "2020-11-27T12:00:20.000000"),
        (1, 5, "We don't know Spanish!", "2020-11-27T12:30:00.000000"),
        (5, 1, "Lol certainly we don't", "2021-11-27T12:00:10.000000"),
        (1, 5, "Could you spare 1mil dollars?", "2021-11-27T12:00:20.000000"),
        (5, 1, "Yeah...goodbye.", "2021-11-27T12:30:00.000000"),
    ]

    for message_template in message_templates:
        msg = ChatMessage({
            "user_connection_id": 4,
            "sender_user_id": message_template[0],
            "recipient_user_id": message_template[1],
            "body": message_template[2],
        })
        msg.created_at = message_template[3]
        db.session.add(msg)
    db.session.commit()

    # Yield users data for testing purposes
    yield message_templates


@pytest.fixture(scope="function")
def login_client(client, headers):
    """
    Provides a means to quickly change the
    session token on the client and return
    the api response from the login.
    """
    def login(user_email):
        login_url = "/api/sessions"
        data = {
            "email": user_email,
            "password": "Password1234$"
        }
        response = client.post(
            login_url,
            data=json.dumps(data),
            headers=headers)
        return response
    yield login
