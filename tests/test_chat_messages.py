from copy import deepcopy
import json
import pytest


from ._utilities import client, headers
from ._utilities import database_seed_demo_users, login_client
from ._utilities import database_seed_demo_connections_from_user_a
from ._utilities import database_seed_demo_message_user_a_and_b


# * ===========================================================================
# * POST
# * ===========================================================================


def test_message_post_success(
        client, headers, login_client,
        database_seed_demo_connections_from_user_a):
    # Arrange
    request_body = {
        "body": "Are you still there???",
    }
    # Act
    login = login_client("database_user_a@example.com")
    url = "/api/user_connections/4/messages"
    response = client.post(
        url,
        data=json.dumps(request_body),
        headers=headers)
    # Response assertions
    assert response.status_code == 201
    assert response.json.get("message") == "Success"
    assert response.json.get("data") == {
        "id": 1,
        "userConnectionId": 4,
        "senderUserId": 1,
        "senderUserFirstName": "Angelica",
        "senderUserLastName": "Ashworthy",
        "body": "Are you still there???",
    }


def test_message_post_fails_user_not_associated_with_connection(
        client, headers, login_client,
        database_seed_demo_connections_from_user_a):
    # Arrange
    request_body = {
        "body": "Are you still there???",
    }
    # Act
    login = login_client("database_user_b@example.com")
    url = "/api/user_connections/4/messages"
    response = client.post(
        url,
        data=json.dumps(request_body),
        headers=headers)
    # Response assertions
    assert response.status_code == 403
    assert response.json.get("message") == "User is not associated with this connection."  # noqa


def test_message_post_fails_message_body_empty(
        client, headers, login_client,
        database_seed_demo_connections_from_user_a):
    # Arrange
    request_body = {
        "body": "",
    }
    # Act
    login = login_client("database_user_a@example.com")
    url = "/api/user_connections/4/messages"
    response = client.post(
        url,
        data=json.dumps(request_body),
        headers=headers)
    # Response assertions
    assert response.status_code == 400
    assert response.json.get("message") == "The message body cannot be empty."


# * ===========================================================================
# * GET
# * ===========================================================================


def test_get_messages_after_date_success_1(
        client, headers, login_client,
        database_seed_demo_message_user_a_and_b):
    # Arrange
    url = "/api/user_connections/1/messages/datetime?after=2020-11-27T12:00:00.000000"  # noqa
    # Act
    login = login_client("database_user_a@example.com")
    response = client.get(url)
    # Response assertions
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert len(response.json.get("data")) == 6


def test_get_messages_after_date_success_2(
        client, headers, login_client,
        database_seed_demo_message_user_a_and_b):
    # Arrange
    url = "/api/user_connections/1/messages/datetime?after=2021-11-27T12:00:00.000000"  # noqa
    # Act
    login = login_client("database_user_a@example.com")
    response = client.get(url)
    # Response assertions
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert len(response.json.get("data")) == 3


def test_get_messages_after_date_fails_user_not_associated_with_connection(
        client, headers, login_client,
        database_seed_demo_message_user_a_and_b):
    # Arrange
    url = "/api/user_connections/1/messages/datetime?after=2021-11-27T12:00:00.000000"  # noqa
    # Act
    login = login_client("database_user_c@example.com")
    response = client.get(url)
    # Response assertions
    assert response.status_code == 403
    assert response.json.get("message") == "User is not associated with this connection."  # noqa


def test_get_messages_get_by_quantity_with_offset_success_1(
        client, headers, login_client,
        database_seed_demo_message_user_a_and_b):
    # Arrange
    url = "/api/user_connections/1/messages/range?offset=0&quantity=3"
    # Act
    login = login_client("database_user_b@example.com")
    response = client.get(url)
    # Response assertions
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert response.json.get("data")[0]["id"] == 6


def test_get_messages_get_by_quantity_with_offset_success_2(
        client, headers, login_client,
        database_seed_demo_message_user_a_and_b):
    # Arrange
    url = "/api/user_connections/1/messages/range?offset=3&quantity=3"
    # Act
    login = login_client("database_user_b@example.com")
    response = client.get(url)
    # Response assertions
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert response.json.get("data")[0]["id"] == 3


def test_get_last_success(
        client, headers, login_client,
        database_seed_demo_message_user_a_and_b):
    assert False, "Not implemented"


def test_get_last_fails_no_messages(
        client, headers, login_client,
        database_seed_demo_connections_from_user_a):
    # Arrange
    url = "/api/user_connections/1/messages/range?offset=3&quantity=3"
    # Act
    login = login_client("database_user_b@example.com")
    response = client.get(url)
    # Response assertions
    assert response.status_code == 404
    assert response.json.get("message") == "No messages were found."


# * ===========================================================================
# * PATCH
# * ===========================================================================


def test_patch_message_success(
        client, headers, login_client,
        database_seed_demo_message_user_a_and_b):
    assert False, "Not implemented"


def test_patch_message_fails_not_found(
        client, headers, login_client,
        database_seed_demo_message_user_a_and_b):
    assert False, "Not implemented"


def test_patch_message_fails_user_not_sender(
        client, headers, login_client,
        database_seed_demo_message_user_a_and_b):
    assert False, "Not implemented"


def test_patch_delete_message_success(
        client, headers, login_client,
        database_seed_demo_message_user_a_and_b):
    assert False, "Not implemented"


def test_patch_delete_message_fails_not_found(
        client, headers, login_client,
        database_seed_demo_message_user_a_and_b):
    assert False, "Not implemented"


def test_patch_delete_message_fails_user_not_sender(
        client, headers, login_client,
        database_seed_demo_message_user_a_and_b):
    assert False, "Not implemented"


def test_patch_delete_message_cannot_be_read(
        client, headers, login_client,
        database_seed_demo_message_user_a_and_b):
    assert False, "Not implemented"
