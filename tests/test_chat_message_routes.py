from copy import deepcopy
import json
import pytest


from ._fixtures import client, headers
from ._fixtures import database_user_a, database_user_a_login
from ._fixtures import database_user_b, database_user_b_login
from ._fixtures import database_user_c, database_user_c_login
from .test_user_connection_routes import connection_a_to_b
from .test_user_connection_routes import connection_a_to_b_establish


from models import db, User, UserConnection, ChatMessage
from app import app

# Mock user conversation
mock_conversation = [
    (1, "User A: message #1 @ 2019-11-17T14:20:00.000000", "2019-11-17T14:20:00.000000"),  # noqa
    (2, "User A: message #2 @ 2019-11-17T14:21:00.000000", "2019-11-17T14:21:00.000000"),  # noqa
    (1, "User A: message #3 @ 2019-11-17T14:22:00.000000", "2019-11-17T14:22:00.000000"),  # noqa
    (2, "User A: message #4 @ 2019-11-17T14:23:00.000000", "2019-11-17T14:23:00.000000"),  # noqa
    (1, "User A: message #5 @ 2019-11-17T14:24:00.000000", "2019-11-17T14:24:00.000000"),  # noqa
    (2, "User A: message #6 @ 2019-11-17T14:25:00.000000", "2019-11-17T14:25:00.000000"),  # noqa
    (1, "User A: message #7 @ 2019-11-17T14:26:00.000000", "2019-11-17T14:26:00.000000"),  # noqa
    (2, "User A: message #8 @ 2019-11-17T14:27:00.000000", "2019-11-17T14:27:00.000000"),  # noqa
    (1, "User A: message #9 @ 2020-11-17T14:20:00.000000", "2020-11-17T14:20:00.000000"),  # noqa
    (2, "User A: message #10 @ 2020-11-17T14:21:00.000000", "2020-11-17T14:21:00.000000"),  # noqa
    (1, "User A: message #11 @ 2020-11-17T14:22:00.000000", "2020-11-17T14:22:00.000000"),  # noqa
    (2, "User A: message #12 @ 2020-11-17T14:23:00.000000", "2020-11-17T14:23:00.000000"),  # noqa
    (1, "User A: message #13 @ 2020-11-17T14:24:00.000000", "2020-11-17T14:24:00.000000"),  # noqa
    (2, "User A: message #14 @ 2020-11-17T14:25:00.000000", "2020-11-17T14:25:00.000000"),  # noqa
    (1, "User A: message #15 @ 2020-11-17T14:26:00.000000", "2020-11-17T14:26:00.000000"),  # noqa
    (2, "User A: message #16 @ 2020-11-17T14:27:00.000000", "2020-11-17T14:27:00.000000"),  # noqa
]


@pytest.fixture(scope="function")
def mock_a_b_message_history(
        client,
        headers):

    for message in mock_conversation:
        db_message = ChatMessage(message[0], message[1])
        db_message.user_connection_id = 1
        db_message.created_at = message[2]
        db.session.add(db_message)
    db.session.commit()


def test_a_1_post_message_succeeds(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login,
        connection_a_to_b_establish):

    # Arrangement
    url = "/api/user_connections/1/messages"
    message_1 = "Greetings from outer space!"
    message_2 = "Greetings from Earth!"
    data_1 = {
        "body": message_1
    }
    data_2 = {
        "body": message_2
    }

    # Action
    response = client.post(url, data=json.dumps(data_1), headers=headers)

    # Response assertions
    assert response.status_code == 201
    assert response.json.get("message") == "Success"
    assert response.json.get("data")["id"] == 1
    assert response.json.get("data")["userConnectionId"] == 1
    assert response.json.get("data")["body"] == message_1

    # Database assertions
    connection = UserConnection.query.get(1)
    chat_message = ChatMessage.query.get(1)
    assert chat_message.id == 1
    assert chat_message.user_connection_id == 1
    assert chat_message.sender_user_id == 2
    assert chat_message.body == message_1
    assert chat_message.deleted is False
    assert chat_message.updated is False
    assert len(connection.messages) == 1


def test_a_2_post_message_fails_nonexistent_connection(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login,
        connection_a_to_b_establish):

    # Arrangement
    url = "/api/user_connections/9999/messages"
    data = {
        "body": "Greetings from outer space!"
    }

    # Action
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assertions
    assert response.status_code == 404
    assert response.json.get("message") == "A connection was not found with the provided id."  # noqa


def test_a_3_post_message_fails_connection_not_established(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login):

    # Arrangement
    url = "/api/user_connections/1/messages"
    data = {
        "body": "Greetings from outer space!"
    }

    # Action
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Assertions
    assert response.status_code == 400
    assert response.json.get("message") == "Connection is not yet established."  # noqa


def test_b_1_get_messages_after_datetime_success(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login,
        connection_a_to_b_establish,
        mock_a_b_message_history):

    # Arrangement
    url = "/api/user_connections/1/messages/d"
    request_params_a = url + "?after=2019-11-17T14:10:00.000000"
    request_params_b = url + "?after=2020-11-17T14:10:00.000000"
    request_params_c = url + "?after=2020-11-17T14:26:59.000009"

    # Action
    response = client.get(request_params_a)

    # Assertions
    chat_history_length = len(response.json.get("data"))
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert chat_history_length == 16


def test_b_2_get_messages_with_offset_success(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login,
        connection_a_to_b_establish,
        mock_a_b_message_history):

    # Arrangement
    url = "/api/user_connections/1/messages/o"
    request_params_a = url + "?offset=0&quantity=5"
    request_params_b = url + "?offset=5&quantity=5"
    request_params_c = url + "?offset=10&quantity=5"
    request_params_d = url + "?offset=15&quantity=5"

    # Action
    response = client.get(request_params_a)

    # Assertions
    chat_history_length = len(response.json.get("data"))
    first_message_body = response.json.get("data")[0]["body"]
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert "#1" in first_message_body
    assert chat_history_length == 5

    # Action
    response = client.get(request_params_b)

    # Assertions
    chat_history_length = len(response.json.get("data"))
    first_message_body = response.json.get("data")[0]["body"]
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert "#6" in first_message_body
    assert chat_history_length == 5

    # Action
    response = client.get(request_params_c)

    # Assertions
    chat_history_length = len(response.json.get("data"))
    first_message_body = response.json.get("data")[0]["body"]
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert "#11" in first_message_body
    assert chat_history_length == 5

    # Action
    response = client.get(request_params_d)

    # Assertions
    chat_history_length = len(response.json.get("data"))
    first_message_body = response.json.get("data")[0]["body"]
    assert response.status_code == 200
    assert response.json.get("message") == "Success"
    assert "#16" in first_message_body
    assert chat_history_length == 1


def test_b_3_get_messages_with_offset_fails_out_of_range(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login,
        connection_a_to_b_establish,
        mock_a_b_message_history):

    # Arrangement
    url = "/api/user_connections/1/messages/o?offset=9999&quantity=30"

    # Action
    response = client.get(url)

    # Assertions
    assert response.status_code == 404
    assert response.json.get("message") == "Message offset out of range and yielded no results."  # noqa


def test_c_1_patch_message_succeeds(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login,
        connection_a_to_b_establish,
        mock_a_b_message_history):

    # Arrangement
    url = "/api/user_connections/1/messages"
    data = {
        "id": 2,
        "body": "Greetings from the planet Pluto!"
    }

    # Action
    response = client.patch(url, data=json.dumps(data), headers=headers)

    # Assertions
    assert response.status_code == 200
    assert response.json.get("message") == "Success"


def test_c_2_patch_message_fails_message_nonexistent(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login,
        connection_a_to_b_establish,
        mock_a_b_message_history):

    # Arrangement
    url = "/api/user_connections/1/messages"
    data = {
        "id": 9999,
        "body": "Greetings from the planet Pluto!"
    }

    # Action
    response = client.patch(url, data=json.dumps(data), headers=headers)

    # Assertions
    assert response.status_code == 404
    assert response.json.get("message") == "A message was not found with the provided id."  # noqa


def test_c_3_patch_message_fails_user_not_sender(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login,
        connection_a_to_b_establish,
        mock_a_b_message_history):

    # Arrangement
    url = "/api/user_connections/1/messages"
    data = {
        "id": 1,
        "body": "Greetings from the planet Pluto!"
    }

    # Action
    response = client.patch(url, data=json.dumps(data), headers=headers)

    # Assertions
    assert response.status_code == 400
    assert response.json.get("message") == "User is not the sender of this message."  # noqa


def test_d_1_delete_message_succeeds(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login,
        connection_a_to_b_establish,
        mock_a_b_message_history):

    # Arrangement
    url = "/api/user_connections/1/messages/2"

    # Action
    response = client.delete(url, headers=headers)

    # Assertions
    assert response.status_code == 200
    assert response.json.get("message") == "Success"  # noqa


def test_d_2_delete_message_fails_message_nonexistent(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login,
        connection_a_to_b_establish,
        mock_a_b_message_history):

    # Arrangement
    url = "/api/user_connections/1/messages/9999"

    # Action
    response = client.delete(url, headers=headers)

    # Assertions
    assert response.status_code == 404
    assert response.json.get("message") == "A message was not found with the provided id."  # noqa


def test_d_3_delete_message_fails_user_not_sender(
        client,
        headers,
        database_user_a,
        database_user_b,
        database_user_a_login,
        connection_a_to_b,
        database_user_b_login,
        connection_a_to_b_establish,
        mock_a_b_message_history):

    # Arrangement
    url = "/api/user_connections/1/messages/1"

    # Action
    response = client.delete(url, headers=headers)

    # Assertions
    assert response.status_code == 400
    assert response.json.get("message") == "User is not the sender of this message."  # noqa
