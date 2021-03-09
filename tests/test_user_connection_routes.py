from copy import deepcopy
import json
import pytest


from ._fixtures import client, headers
from ._fixtures import database_user_a, database_user_a_login
from ._fixtures import database_user_b, database_user_b_login


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

    # Response assertions
    assert response.status_code == 200
    assert response.json.get("message") == "Success"

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
    db_user_connection = UserConnection.query.get(1)
    db_user_connection is None


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
        "establish": False
    }

    # Act
    response = client.patch(url, data=json.dumps(data), headers=headers)

    # Assert
    assert response.status_code == 400
    assert response.json.get("message") == "User is not the recipient for this connection."  # noqa
