from flask.cli import AppGroup
from .users_seed import seed_users, seed_undo_users
from .user_connections_seed import seed_user_connections, seed_undo_user_connections


seed_commands = AppGroup("seed")


@seed_commands.command("all")
def seed_all():
    seed_users()
    seed_user_connections()


@seed_commands.command("undo")
def seed_undo_all():
    seed_undo_user_connections()
    seed_undo_users()
