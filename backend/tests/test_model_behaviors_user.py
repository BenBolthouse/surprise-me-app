from copy import deepcopy
from datetime import datetime
import json
import pytest


from tests import seed, http_client


from models import db, User


example_user_data = {
    "password": "Password1234$",
    "first_name": "test_first_name",
    "last_name": "test_last_name",
    "email": "test_email@website.com",
    "share_location": True,
    "coord_lat": 12.123456,
    "coord_long": 123.12345,
}


def test_assert_USER_object_CAN_BE_CREATED():  # noqa
    # Arrange
    example_user_data_copy = deepcopy(example_user_data)
    # Act
    subject = User(example_user_data_copy)
    # Assert
    assert subject is not None


def test_assert_USER_object_CAN_NOT_STORE_UNPROTECTED_PASSWORDS():  # noqa
    # Arrange
    example_user_data_copy = deepcopy(example_user_data)
    # Act
    subject = User(example_user_data_copy)
    # Assert
    assert "Password1234$" not in subject.password


def test_assert_USER_object_CAN_UPDATE_PROTECTED_PASSWORDS():  # noqa
    # Arrange
    example_user_data_copy = deepcopy(example_user_data)
    subject = User(example_user_data_copy)
    old_hashed_password = subject.hashed_password
    # Act
    subject.password = "NewPassword5432!"
    # Assert
    assert subject.hashed_password != old_hashed_password


def test_assert_USER_object_CAN_SCOPE_TO_JSON(seed):
    # Arrange
    subject = User.query.filter(User.email == "a@email.com").first()
    # Act
    scoped_subject = subject.to_json([
        "connections",
        "notifications",
        "location"
    ])
    # Assert
    assert scoped_subject["id"] >= 1
    assert scoped_subject["firstName"] == "testusera"
    assert scoped_subject["lastName"] == "testusera"
    assert scoped_subject["email"] == "a@email.com"
    assert scoped_subject["shareLocation"] is True
    assert scoped_subject["coordLat"] == "53.3734053"
    assert scoped_subject["coordLong"] == "-6.3695384"
    assert isinstance(scoped_subject["notifications"], list)
    assert isinstance(scoped_subject["connections"], list)
    assert isinstance(scoped_subject["createdAt"], str)  # str of datetime
    assert isinstance(scoped_subject["updatedAt"], str)  # str of datetime


def test_assert_USER_object_CAN_SCOPE_TO_DICT():
    # Arrange
    subject = User.query.filter(User.email == "a@email.com").first()
    # Act
    scoped_subject = subject.to_dict(["connections", "notifications"])
    # Assert
    assert scoped_subject["id"] >= 1
    assert scoped_subject["first_name"] == "testusera"
    assert scoped_subject["last_name"] == "testusera"
    assert scoped_subject["email"] == "a@email.com"
    assert scoped_subject["share_location"] is True
    assert scoped_subject["coord_lat"] == "53.3734053"
    assert scoped_subject["coord_long"] == "-6.3695384"
    assert isinstance(scoped_subject["notifications"], list)
    assert isinstance(scoped_subject["connections"], list)
    assert isinstance(scoped_subject["created_at"], datetime)
    assert isinstance(scoped_subject["updated_at"], datetime)
