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
