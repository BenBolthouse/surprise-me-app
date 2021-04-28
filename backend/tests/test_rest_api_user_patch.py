from copy import deepcopy
from datetime import datetime
import json
import pytest


from tests import seed, http_client, http_headers, user_login


from models import db, User


example_request_body = {
    "coordLat": 123.123456,
    "coordLong": 12.123456,
}


def test_assert_USER_object_CANNOT_BE_UPDATED_without_authorization(seed, http_client, http_headers):  # noqa
    # Arrange
    endpoint = "/api/users"
    # Act
    response = http_client.patch(
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


def test_assert_USER_object_CAN_BE_UPDATED_with_authorization(seed, http_client, http_headers, user_login):  # noqa
    # Arrange
    endpoint = "/api/users"
    user_login("a@email.com")
    # Act
    response = http_client.patch(
        endpoint,
        data=json.dumps(example_request_body),
        headers=http_headers
    )
    # Assert
    message = response.json.get("message")
    data = response.json.get("data")
    code = response.status_code
    assert message == "Success"
    assert data is not None
    assert code == 200
