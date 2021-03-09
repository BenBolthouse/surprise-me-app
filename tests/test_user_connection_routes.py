from copy import deepcopy
import json
import pytest


from ._fixtures import client, headers
from ._fixtures import database_user_a, database_user_a_login
from ._fixtures import database_user_b, database_user_b_login
from ._fixtures import database_user_c, database_user_c_login


from models import db, User, UserConnection, UserNotification
from app import app


@pytest.fixture(scope="function")
def connection_a_to_b(
        client,
        headers):

    url = "api/user_connections"
    data = {
        "connectionUserId": 2
    }
    yield client.post(url, data=json.dumps(data), headers=headers)


@pytest.fixture(scope="function")
def connection_a_to_b_establish(
        client,
        headers):

    url = "api/user_connections/1"
    data = {
        "establish": True
    }
    yield client.patch(url, data=json.dumps(data), headers=headers)


def test_a_1_post_connection_succeeds(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login):

    # Arrangement
    url = "api/user_connections"
    data = {
        "connectionUserId": 2
    }

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Response assertions
    assert response.status_code == 201
    assert response.json.get("message") == "Success"
    assert response.json.get("data") == {
        "id": 1
    }

    # Database assertions
    db_notification = UserNotification.query.get(1)
    db_user_connection = UserConnection.query.get(1)
    assert db_user_connection.connection_user_id == 2
    assert db_notification.notification_type == "USER_CONN_REQ"
    assert db_notification.body == "Demo User sent you a friend request."
    assert "/api/user_connections/1" in db_notification.hook


def test_a_2_post_connection_fails_nonexistent_user(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login):

    # Arrange
    url = "api/user_connections"
    data = {
        "connectionUserId": 9999
    }

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == 404
    assert response.json.get("message") == "A user was not found with the provided id."  # noqa


def test_a_3_post_connection_fails_duplicate(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b):

    # Arrange
    url = "api/user_connections"
    data = {
        "connectionUserId": 2
    }

    # Act
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == 400
    assert response.json.get("message") == "Connection request already exists for this user relationship."  # noqa


def test_b_1_patch_connection_accept_succeeds(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login):

    # Arrange
    url = "/api/user_connections/1"
    data = {
        "establish": True
    }

    # Act
    response = client.patch(url, data=json.dumps(data), headers=headers)
    message = response.json.get("message")
    data = response.json.get("data")

    # Response assertions
    assert response.status_code == 200
    assert message == "Success"
    assert "id" in data and data["id"] == 1
    assert "name" in data and data["name"] == "Demo User"

    # Database assertions
    db_user_connection = UserConnection.query.get(1)
    assert db_user_connection.established_at is not None


def test_b_2_patch_connection_deny_succeeds(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login):

    # Arrange
    url = "/api/user_connections/1"
    data = {
        "establish": False
    }

    # Act
    response = client.patch(url, data=json.dumps(data), headers=headers)

    # Response assertions
    assert response.status_code == 200
    assert response.json.get("message") == "Success"

    # Database assertions
    assert UserConnection.query.get(1) is None


def test_b_3_patch_connection_fails_user_not_recipient(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b):

    # Arrange
    url = "/api/user_connections/1"
    data = {
        "establish": True
    }

    # Act
    response = client.patch(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == 400
    assert response.json.get("message") == "User is not the recipient for this connection."  # noqa


def test_c_1_get_connections_succeeds(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_c,
        database_user_a_login):
    """
    Tests for the following:

    A. All connections at route
    `/api/user_connections` returns
    established and pending connections.

    B. Pending connections at route
    `/api/user_connections/pending` returns
    only pending connections.

    C. Established connections at route
    `/api/user_connections/established`
    returns only established connections.
    """

    # Arrange
    database_users = [
        {
            "id": 2,
            "established_at": None,
        },
        {
            "id": 3,
            "established_at": "2020-12-31T11:59:00.000000",
        },
    ]
    for user in database_users:
        connection = UserConnection(user["id"])
        connection.requestor_user_id = 1
        connection.established_at = user["established_at"]
        db.session.add(connection)
    db.session.commit()

    # * Case A: All Connections
    # Act
    response = client.get("api/user_connections")

    # Assert
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert response.json.get("data") == [
        {
            "id": 1,
            "name": "Demo User",
            "firstName": "Demo",
            "establishedAt": None
        },
        {
            "id": 2,
            "name": "Demo User",
            "firstName": "Demo",
            "establishedAt": "2020-12-31T11:59:00.000000"
        },
    ]

    # * Case B: Pending Connections
    # Act
    response = client.get("api/user_connections/pending")

    # Assert
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert response.json.get("data") == [
        {
            "id": 1,
            "name": "Demo User",
            "firstName": "Demo",
        },
    ]

    # * Case C: Established Connections
    # Act
    response = client.get("api/user_connections/established")

    # Assert
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert response.json.get("data") == [
        {
            "id": 2,
            "name": "Demo User",
            "firstName": "Demo",
        },
    ]
