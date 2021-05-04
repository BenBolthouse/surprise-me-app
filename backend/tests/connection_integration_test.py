from datetime import datetime
import json


from .__fixtures import seed, client, headers, login
from config import Config
from models import Connection, Notification


def test__connections_routes__POST___create(seed, client, headers, login):
    # Assert that user A can create a connection with user C.

    # Arrange
    url = "/api/v1/connections"
    body = {
        "approver_id": 3,
    }

    # Act
    login = login("A@email.com")
    response = client.post(url, data=json.dumps(body), headers=headers)

    # Assert from response
    get = response.json.get
    assert get("message") == "Connection created successfully"
    assert response.status_code == 201

    # Assert from database
    connection = Connection.query.filter(
        Connection._requestor_id == 1,
        Connection._approver_id == 3).first()
    assert connection is not None
    assert connection.approved_at is None

    # Assert that user C receives a connection notification when user A
    # attempts to connect.

    # Assert from database
    notification = Notification.query.filter(Notification._recipient_id == 3).first()
    assert notification.recipient.id == 3
    assert notification.body == "UserA UserA wants to connect"
    assert notification.action == f"{Config.PUBLIC_URL}/connections/4/approval"


def test__connections_routes__POST___create_fails_existing_active_connection(client, headers, login):
    # Assert that user A cannot create a connection with user C if an
    # active connection between the users already exists.

    # Arrange
    url = "/api/v1/connections"
    body = {
        "approver_id": 3
    }

    # Act
    login = login("A@email.com")
    response = client.post(url, data=json.dumps(body), headers=headers)

    # Assert from response
    get = response.json.get
    assert get("message") == "Connection already exists"
    assert response.status_code == 400


def test__connections_routes__GET___retrieve(client, headers, login):
    # Assert that user B can retrieve their connections.

    # Arrange
    url = "/api/v1/connections"

    # Act
    login("B@email.com")
    response = client.get(url, headers=headers)

    # Assert from response
    get = response.json.get
    expected = {
        0: [("id", 1), ("other_user", {
            "id": 1,
            "first_name": "UserA",
            "last_name": "UserA",
        })],
        1: [("id", 2), ("other_user", {
            "id": 3,
            "first_name": "UserC",
            "last_name": "UserC",
        })]
    }
    assert get("message") == "Success"
    assert response.status_code == 200

    # Assert correct data types from response
    for x in expected.items():
        key = x[0]
        props = x[1]
        connection = get("data")[key]
        for y in props:
            prop_key = y[0]
            prop_val = y[1]
            assert prop_key in connection and connection[prop_key] == prop_val


def test__connections_routes__PATCH__approval_fails_not_recipient(client, headers, login):
    # Assert that connection approval fails when user B attempts to approve
    # a connection between users A and C.

    # Arrange
    url = "/api/v1/connections/4/approve"

    # Act
    login("B@email.com")
    response = client.patch(url, headers=headers)

    # Assert from response
    get = response.json.get
    assert get("message") == "User not approver"
    assert response.status_code == 403

    # Assert that connection approval fails when user A attempts to approve
    # a connection between users A and C, where user C is the recipient.

    # Act
    login("A@email.com")
    response = client.patch(url, headers=headers)

    # Assert from response
    get = response.json.get
    assert get("message") == "User not approver"
    assert response.status_code == 403


def test__connections_routes__PATCH__approval(client, headers, login):
    # Assert that connection approval succeeds when user C attempts to approve
    # a connection between users A and C where user C is the recipient.

    # Arrange
    url = "/api/v1/connections/4/approve"

    # Act
    login("C@email.com")
    response = client.patch(url, headers=headers)

    # Assert from response
    get = response.json.get
    assert get("message") == "Connection approved successfully"
    assert response.status_code == 200


def test__connections_routes__PATCH__denial_fails_not_recipient(client, headers, login):
    # Assert that connection approval fails when user A attempts to deny
    # a connection between users B and C.

    # Arrange
    url = "/api/v1/connections/2/deny"

    # Act
    login("A@email.com")
    response = client.patch(url, headers=headers)

    # Assert from response
    get = response.json.get
    assert get("message") == "User not approver"
    assert response.status_code == 403

    # Assert that connection approval fails when user B attempts to approve
    # a connection between users B and C, where user C is the recipient.

    # Act
    login("B@email.com")
    response = client.patch(url, headers=headers)

    # Assert from response
    get = response.json.get
    assert get("message") == "User not approver"
    assert response.status_code == 403


def test__connections_routes__PATCH__denial(client, headers, login):
    # Assert that connection denial succeeds when user C attempts to deny
    # a connection between users A and C where user C is the recipient.

    # Arrange
    url = "/api/v1/connections/4/deny"

    # Act
    login("C@email.com")
    response = client.patch(url, headers=headers)

    # Assert from response
    get = response.json.get
    assert get("message") == "Connection denied successfully"
    assert response.status_code == 200


def test__connections_routes__DELETE__soft_delete_fails_user_not_member(client, headers, login):
    # Assert that connection deletion fails when user B attempts to deny a
    # connection between users A and C.

    # Arrange
    url = "/api/v1/connections/4"

    # Act
    login("B@email.com")
    response = client.delete(url, headers=headers)

    # Assert from response
    get = response.json.get
    assert get("message") == "User not member"
    assert response.status_code == 403


def test__connections_routes__DELETE__soft_delete(client, headers, login):
    # Assert that connection deletion succeeds when user A attempts to deny
    # a connection between users A and C.

    # Arrange
    url = "/api/v1/connections/4"

    # Act
    login("A@email.com")
    response = client.delete(url, headers=headers)

    # Assert from response
    get = response.json.get
    assert get("message") == "Connection deleted successfully"
    assert response.status_code == 200

    # Assert from database
    connection = Connection.query.filter(
        Connection._requestor_id == 1,
        Connection._approver_id == 3).first()
    assert connection.deleted_at is not None
    assert connection.approved_at is None


def test__connections_routes__POST___create_restores_deleted_connection(client, headers, login):
    # Assert that user C can restore a connection with user A that has
    # previously been deleted, and C now becomes the requestor of the
    # connection.

    # Arrange
    url = "/api/v1/connections"
    body = {
        "approver_id": 1,
    }

    # Act
    login = login("C@email.com")
    response = client.post(url, data=json.dumps(body), headers=headers)

    # Assert from response
    get = response.json.get
    assert get("message") == "Existing connection restored"
    assert response.status_code == 200

    # Assert from database
    connection = Connection.query.filter(
        Connection._requestor_id == 3,
        Connection._approver_id == 1).first()
    assert connection.deleted_at is None
    assert connection.approved_at is None
    assert connection.requestor_id == 3
    assert connection.approver_id == 1

    # Assert that user A receives a connection notification when user C
    # attempts to connect.

    # Assert from database
    notification = Notification.query.filter(Notification._recipient_id == 1).first()
    assert notification.recipient.id == 1
    assert notification.body == "UserC UserC wants to connect"
    assert notification.action == f"{Config.PUBLIC_URL}/connections/4/approval"
