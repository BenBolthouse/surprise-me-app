from copy import deepcopy
import json
import pytest
import flask


from models import db, User, UserConnection, UserNotification
from app import app


@pytest.fixture(scope="module")
def client(request):

    # Yield the application context
    with app.test_client() as client:
        with app.app_context():
            yield client

            # Remove all data from all tables and reset auto increment
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                print('Clear table %s' % table)
                db.engine.execute(table.delete())
                db.engine.execute("ALTER SEQUENCE %s_id_seq RESTART WITH 1;" % table)  # noqa
            db.session.commit()


@pytest.fixture(scope="module")
def headers(client):

    response = client.get("/api/csrf")

    yield {
        "Content-Type": "application/json",
        "Allow": "application/json",
        "X-CSRFToken": response.json["data"]["token"]
    }


user_request_template = {
    "password": "Du&&?121",
    "firstName": "Demo",
    "lastName": "User",
    "email": "demoUser@email.com",
    "shareLocation": True,
    "coordLat": 123.123456,
    "coordLong": 12.123456
}


@pytest.fixture(scope="module")
def database_user_a(client, headers):
    url = "/api/users"
    data = deepcopy(user_request_template)
    data["email"] = "test_user_a@example.com"

    client.post(url, data=json.dumps(data), headers=headers)


@pytest.fixture(scope="module")
def database_user_b(client, headers):
    url = "/api/users"
    data = deepcopy(user_request_template)
    data["email"] = "test_user_b@example.com"

    client.post(url, data=json.dumps(data), headers=headers)


@pytest.fixture(scope="module")
def database_user_a_login(client, headers, database_user_a):
    url = "/api/sessions"
    data = {
        "password": "Du&&?121",
        "email": "test_user_a@example.com",
    }

    client.post(url, data=json.dumps(data), headers=headers)


@pytest.fixture(scope="module")
def database_user_b_login(client, headers, database_user_b):
    url = "/api/sessions"
    data = {
        "password": "Du&&?121",
        "email": "test_user_b@example.com",
    }

    client.post(url, data=json.dumps(data), headers=headers)


@pytest.fixture(scope="module")
def connection_a_to_b(client,
                      headers,
                      database_user_a,
                      database_user_b,
                      database_user_a_login):
    url = "api/user_connections"
    data = {
        "connectionUserId": 2
    }

    yield client.post(url, data=json.dumps(data), headers=headers)


def test_post_connection_succeeds(client,
                                  headers,
                                  database_user_a,
                                  database_user_b,
                                  database_user_a_login,
                                  connection_a_to_b):
    # Act
    response = connection_a_to_b

    # Expected result
    status_code = 201
    message = "success"
    expected_data = {
        "id": 1
    }
    notification = UserNotification.query.get(1)
    connection = UserConnection.query.get(1)

    # Assert
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert response.json.get("data") == expected_data
    assert notification.notification_type == "USER_CONN_REQ"
    assert notification.body == "Demo User sent you a friend request."
    assert "/api/user_connections/1" in notification.hook
    assert connection.connection_user_id == 2


def test_post_connection_fails_nonexistent_user(client,
                                                headers,
                                                database_user_a,
                                                database_user_b,
                                                database_user_a_login,
                                                connection_a_to_b):
    # Arrange
    url = "api/user_connections"
    data = {
        "connectionUserId": 9999
    }

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Expected result
    status_code = 400
    message = "connection_user_nonexistent"

    # Assert
    assert response.status_code == status_code
    assert response.json.get("message") == message


def test_patch_connection_accept_succeeds(client,
                                          headers,
                                          database_user_a,
                                          database_user_b,
                                          database_user_b_login,
                                          connection_a_to_b):
    # Arrange
    url = "/api/user_connections/1"
    data = {
        "establish": True
    }

    # Act
    response = client.patch(url, data=json.dumps(data), headers=headers)

    # Expected result
    status_code = 200
    message = "success"
    expected_data = {
        "id": 1
    }

    # Assert
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert response.json.get("data") == expected_data


def test_patch_connection_deny_succeeds(client,
                                        headers,
                                        database_user_a,
                                        database_user_b,
                                        database_user_b_login,
                                        connection_a_to_b):
    # Arrange
    url = "/api/user_connections/1"
    data = {
        "establish": False
    }

    # Act
    response = client.patch(url, data=json.dumps(data), headers=headers)

    # Expected result
    status_code = 200
    message = "success"
    expected_data = "deleted"

    # Assert
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert response.json.get("data") == expected_data
