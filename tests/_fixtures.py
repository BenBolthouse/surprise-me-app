import json
import pytest


from app import app
from models import db


@pytest.fixture(scope="module")
def client():
    """
    Establishes a client context for sending requests to the API. Teardown removes
    all records from all database tables and resets primary key sequences to 1.
    """
    with app.test_client() as client:
        with app.app_context():
            yield client
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                print('Clear table %s' % table)
                db.engine.execute(table.delete())
                db.engine.execute("ALTER SEQUENCE %s_id_seq RESTART WITH 1;" % table)  # noqa
            db.session.commit()


@pytest.fixture(scope="module")
def headers(client):
    """
    Requests an anti-csrf token from the API and returns a header object for
    client POST, PATCH and DELETE requests.
    """
    response = client.get("/api/csrf")
    yield {
        "Content-Type": "application/json",
        "Allow": "application/json",
        "X-CSRFToken": response.json.get("data")["token"]
    }


@pytest.fixture(scope="module")
def database_user_a(client, headers):
    """
    Creates a sample user A in the database, distint from other sample users.
    Returns the user template data.
    """
    url = "/api/users"
    data = {
        "password": "Du&&?121",
        "firstName": "Demo",
        "lastName": "User",
        "email": "database_user_a@example.com",
        "shareLocation": True,
        "coordLat": 123.123456,
        "coordLong": 12.123456
    }
    client.post(url, data=json.dumps(data), headers=headers)
    yield data


@pytest.fixture(scope="module")
def database_user_b(client, headers):
    """
    Creates a sample user B in the database, distint from other sample users.
    Returns the user template data.
    """
    url = "/api/users"
    data = {
        "password": "Du&&?121",
        "firstName": "Demo",
        "lastName": "User",
        "email": "database_user_b@example.com",
        "shareLocation": True,
        "coordLat": 123.123456,
        "coordLong": 12.123456
    }
    client.post(url, data=json.dumps(data), headers=headers)
    yield data


@pytest.fixture(scope="module")
def database_user_c(client, headers):
    """
    Creates a sample user C in the database, distint from other sample users.
    Returns the user template data.
    """
    url = "/api/users"
    data = {
        "password": "Du&&?121",
        "firstName": "Demo",
        "lastName": "User",
        "email": "database_user_c@example.com",
        "shareLocation": True,
        "coordLat": 123.123456,
        "coordLong": 12.123456
    }
    client.post(url, data=json.dumps(data), headers=headers)
    yield data


# Database user logins

def database_user_a_login(client, headers):
    """
    Provides a session login cookie for sample user A.
    """
    url = "/api/sessions"
    data = {
        "password": "Du&&?121",
        "email": "database_user_a@example.com",
    }
    response = client.post(url, data=json.dumps(data), headers=headers)
    return client


def database_user_b_login(client, headers):
    """
    Provides a session login cookie for sample user B.
    """
    url = "/api/sessions"
    data = {
        "password": "Du&&?121",
        "email": "database_user_b@example.com",
    }
    response = client.post(url, data=json.dumps(data), headers=headers)
    return client


def database_user_c_login(client, headers):
    """
    Provides a session login cookie for sample user C.
    """
    url = "/api/sessions"
    data = {
        "password": "Du&&?121",
        "email": "database_user_c@example.com",
    }
    response = client.post(url, data=json.dumps(data), headers=headers)
    return client
