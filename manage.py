from flask_script import Manager

from staaxe.app import app, db
from staaxe.models import App, Connection, Payload, ConnectionInfo, Metadata

from scripts import import_v1sqlite, export_to_json


manager = Manager(app)

@manager.command
def initdb():
    db.database.connect()
    db.database.create_tables([App, Connection, Payload, ConnectionInfo, Metadata])
    Metadata.create()
    db.database.close()


@manager.command
def game(name):
    """ Return the token for a designed game. Create it if not already exists."""
    db.database.connect()
    game, created = App.get_or_create(name=name)
    if isinstance(game.token, str):
        print("Token :", game.token)
    else:
        print("Token :", game.token.hex)
    db.database.close()

@manager.command
def import_from_v1(filename):
    with db.database.atomic():
        import_v1sqlite.import_from_v1sqlite(filename)

@manager.command
def export_json(appname):
    export_to_json.export_to_json(appname)

if __name__ == "__main__":
    manager.run()

