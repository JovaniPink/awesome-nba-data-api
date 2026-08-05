"""Flask CLI and development entry point."""

from app import create_app
from app.commands import init_db_command

connexion_app = create_app()
app = connexion_app.app
app.cli.add_command(init_db_command)


if __name__ == "__main__":
    connexion_app.run(port=5000)
