from flask import Blueprint


from .production.connections import up as production_connections_up
from .production.messages import up as production_messages_up
from .production.notifications import up as production_notifications_up
from .production.products import up as production_products_up
from .production.users import up as production_users_up

from .test.connections import up as test_connections_up
from .test.messages import up as test_messages_up
from .test.users import up as test_users_up

from .undo.connections import down as connections_down
from .undo.messages import down as messages_down
from .undo.notifications import down as notifications_down
from .undo.products import down as products_down
from .undo.users import down as users_down

from models import db


cmd = Blueprint("seed", __name__)


def test():
    test_users_up()
    test_connections_up()
    test_messages_up()


def down():
    notifications_down()
    messages_down()
    connections_down()
    users_down()


@cmd.cli.command("all")
def cli_all():
    production_users_up()
    production_connections_up()
    production_messages_up()
    production_notifications_up()
    production_products_up()


@cmd.cli.command("undo")
def cli_down():
    products_down()
    notifications_down()
    messages_down()
    connections_down()
    users_down()
