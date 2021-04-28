from copy import deepcopy
from datetime import datetime
import json
import pytest


from tests import seed, http_client, http_headers


from models import db, User


example_request_body = {
    "password": "Password1234$",
    "firstName": "testuserk",
    "lastName": "testuserk",
    "email": "k@email.com",
    "shareLocation": True,
    "coordLat": 123.123456,
    "coordLong": 12.123456,
}


def test_assert_USER_object_CAN_BE_CREATED_from_http_post(seed, http_client, http_headers):  # noqa
    # Arrange
    endpoint = "/api/users"
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
    assert message == "Success"
    assert data["id"] == 11
    assert data["firstName"] == "testuserk"
    assert data["lastName"] == "testuserk"
    assert data["email"] == "k@email.com"
    assert code == 201


def test_assert_USER_object_CANNOT_BE_CREATED_invalid_password(http_client, http_headers):  # noqa
    # Arrange
    invalid_passwords = [
        "no-uppercase$4",
        "NO-LOWERCASE$4",
        "NoNumbers$A",
        "NoSpecCharS4",
        "Has Spaces5%",
    ]
    endpoint = "/api/users"
    for password in invalid_passwords:
        example_request_body_copy = deepcopy(example_request_body)
        example_request_body_copy["password"] = password
        # Act
        response = http_client.post(
            endpoint,
            data=json.dumps(example_request_body_copy),
            headers=http_headers
        )
        # Assert
        message = response.json.get("message")
        data = response.json.get("data")
        code = response.status_code
        assert message == "Bad Request"
        assert "regex" in data["password"][0]
        assert code == 400


def test_assert_USER_object_CANNOT_BE_CREATED_invalid_first_name(seed, http_client, http_headers):  # noqa
    # Arrange
    invalid_first_names = [
        "%HASBADCHAR",
        "HAS&BADCHAR",
        "HASBADCHAR#",
        "5HASBADCHAR",
        "HAS9BADCHAR",
        "HASBADCHAR5",
        " HASBADCHAR",
        "HAS BADCHAR",
        "HASBADCHAR "
    ]
    endpoint = "/api/users"
    for first_name in invalid_first_names:
        example_request_body_copy = deepcopy(example_request_body)
        example_request_body_copy["firstName"] = first_name
        # Act
        response = http_client.post(
            endpoint,
            data=json.dumps(example_request_body_copy),
            headers=http_headers
        )
        # Assert
        message = response.json.get("message")
        data = response.json.get("data")
        code = response.status_code
        assert message == "Bad Request"
        assert "regex" in data["firstName"][0]
        assert code == 400


def test_assert_USER_object_CANNOT_BE_CREATED_invalid_last_name(seed, http_client, http_headers):  # noqa
    # Arrange
    invalid_last_names = [
        "%HASBADCHAR",
        "HAS&BADCHAR",
        "HASBADCHAR#",
        "5HASBADCHAR",
        "HAS9BADCHAR",
        "HASBADCHAR5",
        " HASBADCHAR",
        "HAS BADCHAR",
        "HASBADCHAR "
    ]
    endpoint = "/api/users"
    for last_name in invalid_last_names:
        example_request_body_copy = deepcopy(example_request_body)
        example_request_body_copy["lastName"] = last_name
        # Act
        response = http_client.post(
            endpoint,
            data=json.dumps(example_request_body_copy),
            headers=http_headers
        )
        # Assert
        message = response.json.get("message")
        data = response.json.get("data")
        code = response.status_code
        assert message == "Bad Request"
        assert "regex" in data["lastName"][0]
        assert code == 400


def test_assert_USER_object_CANNOT_BE_CREATED_invalid_email(seed, http_client, http_headers):  # noqa
    # Arrange
    invalid_emails = [
        "BAD EMAIL@EXAMPLE.COM",
        "BADEMAIL @EXAMPLE.COM",
        "BADEMAIL@ EXAMPLE.COM",
        "BADEMAIL@EXAMPLE .COM",
        "BADEMAIL@EXAMPLE. COM",
        "BADEMAIL@EXAMPLE.COM ",
    ]
    endpoint = "/api/users"
    for email in invalid_emails:
        example_request_body_copy = deepcopy(example_request_body)
        example_request_body_copy["email"] = email
        # Act
        response = http_client.post(
            endpoint,
            data=json.dumps(example_request_body_copy),
            headers=http_headers
        )
        # Assert
        message = response.json.get("message")
        data = response.json.get("data")
        code = response.status_code
        assert message == "Bad Request"
        assert "regex" in data["email"][0]
        assert code == 400


def test_assert_USER_object_CANNOT_BE_CREATED_duplicate_email(seed, http_client, http_headers):  # noqa
    # Arrange
    duplicate_email = "a@email.com"
    endpoint = "/api/users"
    example_request_body_copy = deepcopy(example_request_body)
    example_request_body_copy["email"] = duplicate_email
    # Act
    response = http_client.post(
        endpoint,
        data=json.dumps(example_request_body_copy),
        headers=http_headers
    )
    # Assert
    message = response.json.get("message")
    data = response.json.get("data")
    code = response.status_code
    assert message == "Bad Request"
    assert data["email"][0] == "The requested email is already in use."
    assert code == 400
