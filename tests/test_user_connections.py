from copy import deepcopy
import json
import pytest


from ._utilities import client, headers
from ._utilities import database_seed_demo_users, login_client
from ._utilities import database_seed_demo_connections_from_user_a


from models import db, User, UserConnection, UserNotification


# * ===========================================================================
# * POST
# * ===========================================================================


def test_user_connection_post_success_creates_notification(
        client, headers, login_client):
    """
    Assert user A can request a connection for user B and that
    the application handles creating a user B notification for
    the request.
    """
    # Arrange
    url = "/api/connections"
    request_body = {
        "recipientUserId": 2,
    }
    # Act
    login = login_client("database_user_a@example.com")
    response = client.post(
        url,
        data=json.dumps(request_body),
        headers=headers)
    # Response assertions
    assert response.status_code == 201
    assert response.json.get("message") == "Success"
    assert response.json.get("data") == {
        "id": 1,
        "recipientUserId": 2,
        "recipientFirstName": "Benny",
        "recipientLastName": "Broomtaker",
    }
    # Database assertions
    db_user_connection = UserConnection.query.get(1)
    db_user_notification = UserNotification.query.get(1)
    assert db_user_connection.established_at is None
    assert db_user_connection.created_at is not None
    assert db_user_notification.id == 1
    assert db_user_notification.user_id == 2
    assert db_user_notification.notification_type == "USER_CONN_REQ"
    assert db_user_notification.hook == "http://localhost:5000/api/connections/1"
    assert db_user_notification.body == "Angelica Ashworthy sent you a friend request."
    assert db_user_notification.read_at is None
    assert db_user_notification.dismissed_at is None
    assert db_user_notification.created_at is not None


def test_user_connection_post_fails_recipient_doesnt_exist(
        client, headers, login_client):
    """
    Assert user A cannot establish a connection with a user that
    doesn't exist in the database with the given recipient user ID.
    """
    # Arrange
    url = "/api/connections"
    request_body = {
        "recipientUserId": 9999,
    }
    # Act
    login = login_client("database_user_a@example.com")
    response = client.post(
        url,
        data=json.dumps(request_body),
        headers=headers)
    # Response assertions
    assert response.status_code == 404
    assert response.json.get("message") == "A user was not found with the provided id."


# * ===========================================================================
# * PATCH
# * ===========================================================================


def test_user_connection_patch_success_accept_creates_notification(
        client, headers, login_client):
    """
    Assert user B can accept user A's request to connect and
    creates a notification for user A.
    """
    # Arrange
    url = "/api/connections"
    request_body = {
        "recipientUserId": 2,
    }
    login = login_client("database_user_a@example.com")
    client.post(
        url,
        data=json.dumps(request_body),
        headers=headers)
    # Act
    url = "/api/connections/1/accept"
    login = login_client("database_user_b@example.com")
    response = client.patch(url, headers=headers)
    # Response assertions
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert response.json.get("data") == {
        "id": 1,
        "recipientUserId": 2,
        "recipientFirstName": "Benny",
        "recipientLastName": "Broomtaker",
    }
    # Database assertions
    db_user_connection = UserConnection.query.get(1)
    db_user_notification = UserNotification.query.get(2)
    assert db_user_connection.established_at is not None
    assert db_user_notification.id == 2
    assert db_user_notification.user_id == 1
    assert db_user_notification.notification_type == "USER_CONN_REQ_ESTABLISHED"
    assert db_user_notification.hook == ""
    assert db_user_notification.body == "Benny Broomtaker accepted your friend request."
    assert db_user_notification.read_at is None
    assert db_user_notification.dismissed_at is None
    assert db_user_notification.created_at is not None


def test_user_connection_patch_success_deny_deletes_request(
        client, headers, login_client):
    """
    Assert user B can accept user A's request to connect and
    creates a notification for user A.
    """
    # Arrange
    url = "/api/connections"
    request_body = {
        "recipientUserId": 2,
    }
    login = login_client("database_user_a@example.com")
    client.post(
        url,
        data=json.dumps(request_body),
        headers=headers)
    # Act
    url = "/api/connections/1/deny"
    login = login_client("database_user_b@example.com")
    response = client.patch(url, headers=headers)
    # Response assertions
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    # Database assertions
    db_user_connection = UserConnection.query.get(1)
    db_user_notification = UserNotification.query.get(2)
    assert db_user_connection is None
    assert db_user_notification is None


def test_user_connection_patch_fails_user_not_associated_with_connection(
        client, headers, login_client):
    """
    Assert user B can accept user A's request to connect and
    creates a notification for user A.
    """
    # Arrange
    url = "/api/connections"
    request_body = {
        "recipientUserId": 2,
    }
    login = login_client("database_user_a@example.com")
    client.post(
        url,
        data=json.dumps(request_body),
        headers=headers)
    # Act
    url = "/api/connections/1/accept"
    login = login_client("database_user_c@example.com")
    response = client.patch(url, headers=headers)
    # Assertions
    assert response.status_code == 403
    assert response.json.get("message") == "User is not the recipient for this connection."


def test_user_connection_patch_fails_requestor_attempts_establishment(
        client, headers, login_client):
    """
    Assert user B can accept user A's request to connect and
    creates a notification for user A.
    """
    # Arrange
    url = "/api/connections"
    request_body = {
        "recipientUserId": 2,
    }
    login = login_client("database_user_a@example.com")
    client.post(
        url,
        data=json.dumps(request_body),
        headers=headers)
    # Act
    url = "/api/connections/1/accept"
    login = login_client("database_user_a@example.com")
    response = client.patch(url, headers=headers)
    # Assertions
    assert response.status_code == 403
    assert response.json.get("message") == "User is not the recipient for this connection."


# * ===========================================================================
# * GET
# * ===========================================================================


def test_user_connection_get_all_sent_pending(
        client, headers, login_client,
        database_seed_demo_connections_from_user_a):
    """
    Assert user A can view pending connection requests.
    """
    # Act
    login = login_client("database_user_a@example.com")
    url = "/api/connections/sent_pending"
    response = client.get(url)
    # Assert
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert response.json.get("data") == [
        {
            "id": 1,
            "recipientUserId": 2,
            "recipientFirstName": "Benny",
            "recipientLastName": "Broomtaker",
        },
        {
            "id": 2,
            "recipientUserId": 3,
            "recipientFirstName": "Charlie",
            "recipientLastName": "Caninetooth",
        },
        {
            "id": 3,
            "recipientUserId": 4,
            "recipientFirstName": "Denise",
            "recipientLastName": "Dogood",
        },
    ]


def test_user_connection_get_all_sent_established(
        client, headers, login_client,
        database_seed_demo_connections_from_user_a):
    """
    Assert user A can view established connection requests.
    """
    # Act
    login = login_client("database_user_a@example.com")
    url = "/api/connections/sent_established"
    response = client.get(url)
    # Assert
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert response.json.get("data") == [
        {
            "id": 4,
            "recipientUserId": 5,
            "recipientFirstName": "Emily",
            "recipientLastName": "Earwhisper",
        },
        {
            "id": 5,
            "recipientUserId": 6,
            "recipientFirstName": "Frank",
            "recipientLastName": "Farquad",
        },
        {
            "id": 6,
            "recipientUserId": 7,
            "recipientFirstName": "Gregory",
            "recipientLastName": "Gearhead",
        },
    ]


def test_user_connection_get_all_sent(
        client, headers, login_client,
        database_seed_demo_connections_from_user_a):
    """
    Assert user A can view all connection requests.
    """
    # Act
    login = login_client("database_user_a@example.com")
    url = "/api/connections/sent"
    response = client.get(url)
    # Assert
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert response.json.get("data") == [
        {
            "id": 1,
            "recipientUserId": 2,
            "recipientFirstName": "Benny",
            "recipientLastName": "Broomtaker",
        },
        {
            "id": 2,
            "recipientUserId": 3,
            "recipientFirstName": "Charlie",
            "recipientLastName": "Caninetooth",
        },
        {
            "id": 3,
            "recipientUserId": 4,
            "recipientFirstName": "Denise",
            "recipientLastName": "Dogood",
        },
        {
            "id": 4,
            "recipientUserId": 5,
            "recipientFirstName": "Emily",
            "recipientLastName": "Earwhisper",
        },
        {
            "id": 5,
            "recipientUserId": 6,
            "recipientFirstName": "Frank",
            "recipientLastName": "Farquad",
        },
        {
            "id": 6,
            "recipientUserId": 7,
            "recipientFirstName": "Gregory",
            "recipientLastName": "Gearhead",
        },
    ]


def test_user_connection_get_all_received(
        client, headers, login_client,
        database_seed_demo_connections_from_user_a):
    """
    Assert user A can view all connection requests.
    """
    # Act
    login = login_client("database_user_b@example.com")
    url = "/api/connections/received"
    response = client.get(url)
    # Assert
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert response.json.get("data") == [
        {
            "id": 1,
            "requestorUserId": 1,
            "requestorFirstName": "Angelica",
            "requestorLastName": "Ashworthy",
            "accept": "/api/connections/1/accept",
            "deny": "/api/connections/1/deny",
        },
    ]


def test_user_delete_cascade_deletes_connections(
        client, headers, login_client,
        database_seed_demo_connections_from_user_a):
    # Arrange
    user_a = User.query.get(1)
    # Assert connection exists
    UserConnection.query.get(1) is not None
    # Act
    db.session.delete(user_a)
    db.session.commit()
    # Assert connection destroyed
    UserConnection.query.get(1) is None
