from copy import deepcopy
import json
import pytest


from ._fixtures import client, headers, clear_chat_messages_records
from ._fixtures import database_user_a, database_user_a_login
from ._fixtures import database_user_b, database_user_b_login
from ._fixtures import database_user_c, database_user_c_login
from .test_user_connection_routes import connection_a_to_b
from .test_user_connection_routes import connection_a_to_b_establish


from models import db, User, UserConnection, ChatMessage
from app import app

# Mock user conversation
mock_conversation = [
    (
        1,
        "User A: message #1 @ 2019-11-17T14:20:00.000000",
        "2019-11-17T14:20:00.000000"
    ),
    (
        2,
        "User A: message #2 @ 2019-11-17T14:21:00.000000",
        "2019-11-17T14:21:00.000000"
    ),
    (
        1,
        "User A: message #3 @ 2019-11-17T14:22:00.000000",
        "2019-11-17T14:22:00.000000"
    ),
    (
        2,
        "User A: message #4 @ 2019-11-17T14:23:00.000000",
        "2019-11-17T14:23:00.000000"
    ),
    (
        1,
        "User A: message #5 @ 2019-11-17T14:24:00.000000",
        "2019-11-17T14:24:00.000000"
    ),
    (
        2,
        "User A: message #6 @ 2019-11-17T14:25:00.000000",
        "2019-11-17T14:25:00.000000"
    ),
    (
        1,
        "User A: message #7 @ 2019-11-17T14:26:00.000000",
        "2019-11-17T14:26:00.000000"
    ),
    (
        2,
        "User A: message #8 @ 2019-11-17T14:27:00.000000",
        "2019-11-17T14:27:00.000000"
    ),
    (
        1,
        "User A: message #9 @ 2020-11-17T14:20:00.000000",
        "2020-11-17T14:20:00.000000"
    ),
    (
        2,
        "User A: message #10 @ 2020-11-17T14:21:00.000000",
        "2020-11-17T14:21:00.000000"
    ),
    (
        1,
        "User A: message #11 @ 2020-11-17T14:22:00.000000",
        "2020-11-17T14:22:00.000000"
    ),
    (
        2,
        "User A: message #12 @ 2020-11-17T14:23:00.000000",
        "2020-11-17T14:23:00.000000"
    ),
    (
        1,
        "User A: message #13 @ 2020-11-17T14:24:00.000000",
        "2020-11-17T14:24:00.000000"
    ),
    (
        2,
        "User A: message #14 @ 2020-11-17T14:25:00.000000",
        "2020-11-17T14:25:00.000000"
    ),
    (
        1,
        "User A: message #15 @ 2020-11-17T14:26:00.000000",
        "2020-11-17T14:26:00.000000"
    ),
    (
        2,
        "User A: message #16 @ 2020-11-17T14:27:00.000000",
        "2020-11-17T14:27:00.000000"
    ),
]


@pytest.fixture(scope="module")
def mock_a_b_message_history(
        client,
        headers,
        connection_a_to_b_establish):

    for message in mock_conversation:
        db_message = ChatMessage(message[0], message[1])
        db_message.user_connection_id = 1
        db_message.created_at = message[2]
        db.session.add(db_message)
    db.session.commit()


def test_post_message_succeeds(
        client,
        headers,
        connection_a_to_b_establish):

    # Arrangement
    url = "/api/user_connections/1/messages"
    user_a_message = "Greetings from outer space!"
    user_b_message = "Greetings from Earth!"
    user_a_data = {
        "body": user_a_message
    }
    user_b_data = {
        "body": user_b_message
    }

    # Test user A...

    # Action
    login_client = database_user_a_login(client, headers)
    response_post_by_a = login_client.post(
        url,
        data=json.dumps(user_a_data),
        headers=headers)

    # Expected results
    status_code = 201
    message = "success"
    db_user_post_by_a_connection = UserConnection.query.get(1)
    db_chat_post_by_a_message = ChatMessage.query.get(1)

    # Response assertions
    assert response_post_by_a.status_code == status_code
    assert response_post_by_a.json.get("message") == message
    assert response_post_by_a.json.get("data")["id"] == 1
    assert response_post_by_a.json.get("data")["userConnectionId"] == 1
    assert response_post_by_a.json.get("data")["body"] == user_a_message

    # Database assertions
    assert db_chat_post_by_a_message.id == 1
    assert db_chat_post_by_a_message.user_connection_id == 1
    assert db_chat_post_by_a_message.sender_user_id == 1
    assert db_chat_post_by_a_message.body == user_a_message
    assert db_chat_post_by_a_message.deleted is False
    assert db_chat_post_by_a_message.updated is False
    assert len(db_user_post_by_a_connection.messages) == 1

    # Now test user B...

    # Action
    login_client = database_user_b_login(client, headers)
    response_post_by_b = login_client.post(
        url,
        data=json.dumps(user_b_data),
        headers=headers)

    # Expected results
    status_code = 201
    message = "success"
    db_user_post_by_b_connection = UserConnection.query.get(1)
    db_chat_post_by_b_message = ChatMessage.query.get(2)

    # Response assertions
    assert response_post_by_b.status_code == status_code
    assert response_post_by_b.json.get("message") == message
    assert response_post_by_b.json.get("data")["id"] == 2
    assert response_post_by_b.json.get("data")["userConnectionId"] == 1
    assert response_post_by_b.json.get("data")["body"] == user_b_message

    # Database assertions
    assert db_chat_post_by_b_message.id == 2
    assert db_chat_post_by_b_message.user_connection_id == 1
    assert db_chat_post_by_b_message.sender_user_id == 2
    assert db_chat_post_by_b_message.body == user_b_message
    assert db_chat_post_by_b_message.deleted is False
    assert db_chat_post_by_b_message.updated is False
    assert len(db_user_post_by_b_connection.messages) == 2

    clear_chat_messages_records()


def test_post_message_fails_nonexistent_connection(
        client,
        headers,
        connection_a_to_b):

    # Arrangement
    url = "/api/user_connections/9999/messages"
    data = {
        "body": "Greetings from outer space!"
    }

    # Action
    login_client = database_user_a_login(client, headers)
    response = login_client.post(url, data=json.dumps(data), headers=headers)

    # Expected results
    status_code = 400
    message = "connection_nonexistent"

    # Assertions
    assert response.status_code == status_code
    assert response.json.get("message") == message


def test_get_messages_after_datetime_success(
        client,
        headers,
        connection_a_to_b,
        mock_a_b_message_history):

    # Arrangement
    url = "/api/user_connections/1/messages/d"
    request_params_a = url + "?after=2019-11-17T14:10:00.000000"
    request_params_b = url + "?after=2020-11-17T14:10:00.000000"
    request_params_c = url + "?after=2020-11-17T14:26:59.000009"

    # Action
    client_login = database_user_a_login(client, headers)
    response = client_login.get(request_params_a)

    # Expected results
    status_code = 200
    message = "success"

    # Assertions
    chat_history_length = len(response.json.get("data")["chat_messages"])
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert chat_history_length == 16

    # Action
    client_login = database_user_b_login(client, headers)
    response = client_login.get(request_params_b)

    # Expected results
    status_code = 200
    message = "success"

    # Assertions
    chat_history_length = len(response.json.get("data")["chat_messages"])
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert chat_history_length == 8

    # Action
    client_login = database_user_a_login(client, headers)
    response = client_login.get(request_params_c)

    # Expected results
    status_code = 200
    message = "success"

    # Assertions
    chat_history_length = len(response.json.get("data")["chat_messages"])
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert chat_history_length == 1


def test_get_messages_with_offset_success(
        client,
        headers,
        connection_a_to_b,
        mock_a_b_message_history):

    # Arrangement
    url = "/api/user_connections/1/messages/o"
    request_params_a = url + "?offset=0&quantity=5"
    request_params_b = url + "?offset=5&quantity=5"
    request_params_c = url + "?offset=10&quantity=5"

    # Action
    client_login = database_user_a_login(client, headers)
    response = client_login.get(request_params_a)

    # Expected results
    status_code = 200
    message = "success"

    # Assertions
    chat_history_length = len(response.json.get("data")["chat_messages"])
    first_message_body = response.json.get("data")["chat_messages"][0]["body"]
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert "#16" in first_message_body
    assert chat_history_length == 5

    # Action
    client_login = database_user_b_login(client, headers)
    response = client_login.get(request_params_b)

    # Expected results
    status_code = 200
    message = "success"

    # Assertions
    chat_history_length = len(response.json.get("data")["chat_messages"])
    first_message_body = response.json.get("data")["chat_messages"][0]["body"]
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert "#11" in first_message_body
    assert chat_history_length == 5

    # Action
    client_login = database_user_a_login(client, headers)
    response = client_login.get(request_params_c)

    # Expected results
    status_code = 200
    message = "success"

    # Assertions
    chat_history_length = len(response.json.get("data")["chat_messages"])
    first_message_body = response.json.get("data")["chat_messages"][0]["body"]
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert "#6" in first_message_body
    assert chat_history_length == 5

    clear_chat_messages_records()
