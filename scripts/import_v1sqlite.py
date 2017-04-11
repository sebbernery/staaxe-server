import dataset

from staaxe.app import db
from staaxe.models import App, Connection, Payload, ConnectionInfo, Metadata


def import_from_v1sqlite(dbfilename):
    old_db = dataset.connect("sqlite:///" + dbfilename)

    for app in old_db["app"].all():
        App.get_or_create(
            token=app["token"],
            name=app["name"]
        )

    connections = old_db["connection"].all()
    for connection in connections:
        new_connection, _ = Connection.get_or_create(
            uuid=connection["uuid"],
            app=App.get(App.token == connection["app_id"]),
            date_start=connection["date_start"]
        )
        new_connection.date_end = connection["date_end"]
        new_connection.messages_count = old_db["message"].count(connection_id=connection["uuid"])

        connection_info = old_db["connectioninfo"].find_one(connection_id=connection["uuid"])

        if connection_info is not None:
            new_connection_info = ConnectionInfo.get_or_create(
                connection=new_connection,
                host=connection_info["host"],
                user_agent=connection_info["user_agent"],
                accept_lang=connection_info["accept_lang"],
                ip_address=connection_info["ip_address"]
            )

        messages = old_db["message"].find(connection_id=connection["uuid"])

        for message in messages:
            since_connection = (message["date"] - new_connection.date_start).total_seconds()

            payloads = old_db["payload"].find(message_id=message["id"])
            for payload in payloads:
                Payload.get_or_create(
                    connection=new_connection,
                    key=payload["key"],
                    value=payload["value"],
                    time_since_connection=since_connection
                )

