from flask.cli import AppGroup


from .test.users import up as test_users_up
from .undo.users import down as users_down


seed_commands = AppGroup("seed")


def test():
    test_users_up()


def down():
    users_down()
