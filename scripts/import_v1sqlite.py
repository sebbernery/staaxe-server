import dataset

from staaxe.models import App, Connection, Payload, ConnectionInfo, Metadata


def import_from_v1sqlite(dbfilename):
    db = dataset.connect("sqlite:///" + dbfilename)

    for app in db["app"].all():
        App.create(
            token=app["token"],
            name=app["name"]
        )

    connections = db["connection"].all()
    for connection in connections:
        new_connection = Connection.create(
            uuid=connection["uuid"],
            app=App.get(App.token == connection["app_id"]),
            date_start=connection["date_start"],
            date_end=connection["date_end"],
            messages_count=db["message"].count(connection_id=connection["uuid"])
        )

        try:
            connection_info = db["connectioninfo"].find_one(connection_id=new_connection.uuid)

            new_connection_info = ConnectionInfo.create(
                connection=new_connection,
                host=connection_info["host"],
                user_agent=connection_info["user_agent"],
                accept_lang=connection_info["accept_lang"],
                ip_address=connection_info["ip_address"]
            )
        except:
            print("ERROR on connection_info")
            pass

        messages = db["message"].find(connection_id=connection["uuid"])

        for message in messages:
            since_connection = (message["date"] - new_connection.date_start).total_seconds()

            payloads = db["payload"].find(message_id=message["id"])
            for payload in payloads:
                Payload.create(
                    connection=new_connection,
                    key=payload["key"],
                    value=payload["value"],
                    time_since_connection=since_connection
                )

