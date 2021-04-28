from copy import deepcopy
from datetime import datetime
import json
import pytest


from tests import seed, http_client, http_headers, user_login


from models import db, User, UserConnection


example_request_body = {
    "recipientUserId": 4,
}


def test_assert_USER_CONNECTION_object_CANNOT_BE_CREATED_without_authorization(seed, http_client, http_headers):  # noqa
    # Arrange
    endpoint = "/api/connections"
    # Act
    response = http_client.post(
        endpoint,
        data=json.dumps(example_request_body),
        headers=http_headers
    )
    # Assert
    message = response.json.get("message")
    data = response.json.get("data")
    code = response.status_code
    assert "Unauthorized"
    assert data is None
    assert code == 401


def test_assert_USER_CONNECTION_object_CAN_BE_CREATED_with_authorization(seed, http_client, http_headers, user_login):  # noqa
    # Arrange
    endpoint = "/api/connections"
    user_login("a@email.com")
    # Act
    response = http_client.post(
        endpoint,
        data=json.dumps(example_request_body),
        headers=http_headers
    )
    # Assert
    message = response.json.get("message")
    data = response.json.get("data")
    code = response.status_code
    assert "Success"
    assert isinstance(data["createdAt"], str)
    assert isinstance(data["establishedAt"], str) or data["establishedAt"] is None
    assert code == 201
