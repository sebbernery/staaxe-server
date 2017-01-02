import json
import uuid

from flask import request, g, jsonify
import peewee

from app import app, db
from models import Connection, App, Message, ConnectionInfo


@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


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

    host = request.referrer or request.headers["Host"]
    user_agent = request.headers["User-Agent"]
    accept_lang = request.headers["Accept-Language"]
    ip_address = request.remote_addr

    with g.db.atomic():
        conn = Connection.create(app=game)
        ConnectionInfo.create(
            connection=conn,
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

    with g.db.atomic():
        added = conn.add_message(data["payload"])

    return jsonify({
        'num_received': added
    })

