from flask.cli import AppGroup


from .test.connections import up as test_connections_up
from .undo.connections import down as connections_down
from .test.users import up as test_users_up
from .undo.users import down as users_down


seed_commands = AppGroup("seed")


def test():
    test_users_up()
    test_connections_up()


def down():
    connections_down()
    users_down()
