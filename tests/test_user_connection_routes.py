from copy import deepcopy
import json
import pytest


from ._fixtures import client, headers
from ._fixtures import database_user_a, database_user_a_login
from ._fixtures import database_user_b, database_user_b_login


from models import db, User, UserConnection, UserNotification
from app import app


@pytest.fixture(scope="module")
def connection_a_to_b(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login):

    url = "api/user_connections"
    data = {
        "connectionUserId": 2
    }

    yield client.post(url, data=json.dumps(data), headers=headers)


def test_post_connection_succeeds(
        client,
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


def test_post_connection_fails_nonexistent_user(
        client,
        headers,
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


def test_patch_connection_accept_succeeds(
        client,
        headers,
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


def test_patch_connection_deny_succeeds(
        client,
        headers,
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
