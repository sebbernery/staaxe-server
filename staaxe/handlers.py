import json
import uuid

from flask import request, g, jsonify
import peewee

from staaxe.app import app, db
from staaxe.models import Connection, App, ConnectionInfo


@app.route("/init", methods=["POST"])
def init():
    data = json.loads(request.data.decode("utf-8"))
    token = uuid.UUID(data["token"])

    try:
        game = App.get(App.token==token)
    except peewee.DoesNotExist:
        return jsonify({
            "error": "Token don't exist."
        })

    referrer = request.referrer
    host = request.headers["Host"]
    user_agent = request.headers["User-Agent"]
    accept_lang = request.headers["Accept-Language"]
    ip_address = request.remote_addr

    with db.database.atomic():
        conn = Connection.create(app=game)
        ConnectionInfo.create(
            connection=conn,
            referrer=referrer,
            host=host,
            user_agent=user_agent,
            accept_lang=accept_lang,
            ip_address=ip_address
        )

    return jsonify({
        'error': None,
        'id': conn.uuid,
    })

@app.route("/send", methods=["POST"])
def send():
    data = json.loads(request.data.decode("utf-8"))
    connection_id = uuid.UUID(data["id"])
    conn = Connection.get(uuid=connection_id)

    with db.database.atomic():
        added = conn.add_message(data["payload"])

    return jsonify({
        'num_received': added
    })

