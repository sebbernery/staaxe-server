from flask_script import Manager

from app import app, db
from models import App, Connection, Message, Payload, ConnectionInfo


manager = Manager(app)

@manager.command
def initdb():
    db.connect()
    db.create_tables([App, Connection, Message, Payload, ConnectionInfo])
    db.close()


@manager.command
def game(name):
    """ Return the token for a designed game. Create it if not already exists."""
    db.connect()
    game, created = App.get_or_create(name=name)
    if isinstance(game.token, str):
        print("Token :", game.token)
    else:
        print("Token :", game.token.hex)
    db.close()


if __name__ == "__main__":
    manager.run()

