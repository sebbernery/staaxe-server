import datetime
import json

from staaxe.models import App, Connection, ConnectionInfo, Payload


def export_to_json(appname):
    app = App.get(App.name == appname)

    ret_obj = {'connections': [], 'metadata': {}}

    first_connection_date = datetime.datetime.now()

    for connection in app.connection_set.order_by(Connection.date_start):
        ret_payloads = []

        payloads = connection.payload_set.order_by(Payload.time_since_connection.asc())
        for msg_idx, payload in enumerate(payloads):
            ret_payloads.append((
                int(payload.time_since_connection),
                payload.key,
                payload.value
            ))

        ret_obj["connections"].append({
            "ds": str(connection.date_start),
            "de": str(connection.date_end),
            "p": ret_payloads,
            "nm": connection.messages_count
        })

        first_connection_date = min(first_connection_date, connection.date_start)

    ret_obj["metadata"]["first_connection_date"] = str(first_connection_date)

    print(json.dumps(ret_obj, separators=(",", ":")))

