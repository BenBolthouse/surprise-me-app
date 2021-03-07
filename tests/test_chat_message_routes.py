from copy import deepcopy
import json
import pytest


from ._fixtures import client, headers
from ._fixtures import database_user_a, database_user_a_login
from ._fixtures import database_user_b, database_user_b_login
from .test_user_connection_routes import connection_a_to_b


from models import db, User, UserConnection, ChatMessage
from app import app


def test_post_message_succeeds(
        client,
        headers,
        database_user_a_login,
        connection_a_to_b):

    # Arrangement
    url = "/api/user_connections/1/messages"
    data = {
        "body": "Greetings from outer space!"
    }

    # Action
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Expected results
    status_code = 201
    message = "success"
    user_connection = UserConnection.query.get(1)
    chat_message = ChatMessage.query.get(1)

    # Assertions
    assert response.status_code == status_code
    assert response.json.get("message") == message
    assert chat_message.body == "Greetings from outer space!"
    assert len(user_connection.messages) == 1


def test_post_message_fails_nonexistent_connection(
        client,
        headers,
        database_user_a_login,
        connection_a_to_b):

    # Arrangement
    url = "/api/user_connections/9999/messages"
    data = {
        "body": "Greetings from outer space!"
    }

    # Action
    response = client.post(url, data=json.dumps(data), headers=headers)

    # Expected results
    status_code = 400
    message = "connection_nonexistent"

    # Assertions
    assert response.status_code == status_code
    assert response.json.get("message") == message
