from flask import Flask
from flask.ext.cors import CORS
from peewee import SqliteDatabase

import config


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

if config.DEBUG:
    app.config['PROPAGATE_EXCEPTIONS'] = True

db = SqliteDatabase(config.DATABASE_NAME)

