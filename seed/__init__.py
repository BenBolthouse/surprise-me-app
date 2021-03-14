from flask.cli import AppGroup
from .chat_messages_seed import seed_chat_messages, seed_undo_chat_messages
from .user_connections_seed import seed_user_connections, seed_undo_user_connections
from .user_notifications_seed import seed_user_notifications, seed_undo_user_notifications
from .users_seed import seed_users, seed_undo_users


seed_commands = AppGroup("seed")


@seed_commands.command("all")
def seed_all():
    seed_users()
    seed_user_connections()
    seed_user_notifications()
    seed_chat_messages()


@seed_commands.command("undo")
def seed_undo_all():
    seed_undo_chat_messages()
    seed_undo_user_notifications()
    seed_undo_user_connections()
    seed_undo_users()
