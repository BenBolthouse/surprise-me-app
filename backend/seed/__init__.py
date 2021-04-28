from flask.cli import AppGroup


seed_commands = AppGroup("seed")


@seed_commands.command("all")
def up():
    pass


@seed_commands.command("undo")
def down():
    pass
