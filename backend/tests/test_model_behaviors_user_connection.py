from copy import deepcopy
from datetime import datetime
import json
import pytest


from tests import seed, http_client, http_headers, user_login


from models import db, User, UserConnection


def test_assert_USER_CONNECTION_object_CAN_BE_CREATED(seed):  # noqa
    # Arrange
    example_user_a = User.query.filter(User.email == "a@email.com").first()
    example_user_d = User.query.filter(User.email == "d@email.com").first()
    # Act
    subject = UserConnection({
        "requestor_user_id": example_user_a.id,
        "recipient_user_id": example_user_d.id,
    })
    # Assert
    assert subject is not None


def test_assert_USER_CONNECTION_object_CAN_SCOPE_TO_JSON(seed):  # noqa
    # Arrange
    example_user_a = User.query.filter(User.email == "a@email.com").first()
    subject_a = UserConnection.query.get(1)  # Requestor A --> recipient B
    # Act
    scoped_subject_a = subject_a.to_json(
        example_user_a.id,
        ["otherUser", "lastMessage"]
    )
    # Assert
    assert isinstance(scoped_subject_a["createdAt"], str)  # datetime
    assert isinstance(scoped_subject_a["establishedAt"], str)  # datetime
    assert scoped_subject_a["otherUser"]["id"] == 2
    assert scoped_subject_a["lastMessage"] is None


def test_assert_USER_CONNECTION_object_CAN_SCOPE_TO_DICT(seed):  # noqa
    # Arrange
    example_user_a = User.query.filter(User.email == "a@email.com").first()
    subject_a = UserConnection.query.get(1)  # Requestor A --> recipient B
    # Act
    scoped_subject_a = subject_a.to_dict(
        example_user_a.id,
        ["other_user", "last_message"]
    )
    # Assert
    assert isinstance(scoped_subject_a["created_at"], datetime)  # datetime
    assert isinstance(scoped_subject_a["established_at"], datetime)  # datetime
    assert scoped_subject_a["other_user"]["id"] == 2
    assert scoped_subject_a["last_message"] is None
