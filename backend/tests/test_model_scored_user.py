import pytest


from .fixtures import seed
from models import db, Connection, ScoredUser


@pytest.fixture(scope="module")
def scored_user():
    '''
    Creates a scored user in the database which emulates a user E to user F
    score.
    '''
    scored_user = ScoredUser(5, 6)

    db.session.add(scored_user)
    db.session.commit()


def test__scored_user__methods__(seed, scored_user):
    # Assert that a connection request from users E to F creates a

    # Act
    pass
