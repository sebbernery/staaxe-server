from flask import Flask
from flask_cors import CORS
from playhouse.flask_utils import FlaskDB

import config


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

if config.DEBUG:
    app.config['PROPAGATE_EXCEPTIONS'] = True

db = FlaskDB(app, config.DATABASE_NAME)

