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
        database_user_b):

    client_login = database_user_a_login(client, headers)
    url = "api/user_connections"
    data = {
        "connectionUserId": 2
    }
    yield client_login.post(url, data=json.dumps(data), headers=headers)


@pytest.fixture(scope="module")
def connection_a_to_b_establish(
        client,
        headers,
        connection_a_to_b):

    client_login = database_user_b_login(client, headers)
    url = "api/user_connections/1"
    data = {
        "establish": True
    }
    yield client_login.patch(url, data=json.dumps(data), headers=headers)


def test_post_connection_succeeds(
        client,
        headers,
        connection_a_to_b):

    # Action
    login_client = database_user_a_login(client, headers)
    response = connection_a_to_b

    # Expected result
    status_code = 201
    message = "success"
    expected_data = {
        "id": 1
    }
    db_notification = UserNotification.query.get(1)
    db_user_connection = UserConnection.query.get(1)

    # Response assertions
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert response.json.get("data") == expected_data

    # Database assertions
    assert db_user_connection.connection_user_id == 2
    assert db_notification.notification_type == "USER_CONN_REQ"
    assert db_notification.body == "Demo User sent you a friend request."
    assert "/api/user_connections/1" in db_notification.hook


def test_post_connection_fails_nonexistent_user(
        client,
        headers,
        connection_a_to_b):

    # Arrange
    url = "api/user_connections"
    data = {
        "connectionUserId": 9999
    }

    # Act
    login_client = database_user_a_login(client, headers)
    response = login_client.post(url, data=json.dumps(data), headers=headers)

    # Expected result
    status_code = 400
    message = "connection_user_nonexistent"

    # Assert
    assert response.status_code == status_code
    assert response.json.get("message") == message


def test_patch_connection_fails_user_not_associated(
        client,
        headers,
        connection_a_to_b):

    # Arrange
    url = "/api/user_connections/1"
    data = {
        "establish": False
    }

    # Act
    login_client = database_user_a_login(client, headers)
    response = login_client.patch(url, data=json.dumps(data), headers=headers)

    # Expected result
    status_code = 404
    message = "connection_nonexistent"

    # Assert
    assert response.status_code == status_code
    assert response.json.get("message") == message


def test_patch_connection_accept_succeeds(
        client,
        headers,
        connection_a_to_b):

    # Arrange
    url = "/api/user_connections/1"
    data = {
        "establish": True
    }

    # Act
    login_client = database_user_b_login(client, headers)
    response = login_client.patch(url, data=json.dumps(data), headers=headers)

    # Expected result
    status_code = 200
    message = "success"
    expected_data = {
        "id": 1
    }
    db_user_connection = UserConnection.query.get(1)

    # Response assertions
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert response.json.get("data") == expected_data

    # Database assertions
    assert db_user_connection.established_at is not None


def test_patch_connection_deny_succeeds(
        client,
        headers,
        connection_a_to_b):

    # Arrange
    url = "/api/user_connections/1"
    data = {
        "establish": False
    }

    # Act
    login_client = database_user_b_login(client, headers)
    response = login_client.patch(url, data=json.dumps(data), headers=headers)

    # Expected result
    status_code = 200
    message = "success"
    expected_data = "deleted"
    db_user_connection = UserConnection.query.get(1)

    # Response assertions
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert response.json.get("data") == expected_data

    # Database assertions
    db_user_connection is None
