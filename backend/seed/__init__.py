from flask.cli import AppGroup


from .test.connections import up as test_connections_up
from .undo.connections import down as connections_down
from .test.messages import up as test_messages_up
from .undo.messages import down as messages_down
from .test.users import up as test_users_up
from .undo.users import down as users_down
from models import db


seed_commands = AppGroup("seed")


def test():
    test_users_up()
    test_connections_up()
    test_messages_up()

    db.session.commit()


def down():
    messages_down()
    connections_down()
    users_down()

    db.session.commit()
