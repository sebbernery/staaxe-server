import datetime
import uuid

from peewee import Model, fn
from peewee import (CharField, DateTimeField, UUIDField, IntegerField, ForeignKeyField,
                    FloatField, TextField)

from staaxe.app import app, db


class BaseModel(db.Model):
    ...

def get_uuid():
    return uuid.uuid4().hex


class App(BaseModel):
    token = UUIDField(index=True, default=get_uuid)
    private_token = UUIDField(default=get_uuid)
    name = CharField(unique=True)
    metadata = TextField(null=True)


class Connection(BaseModel):
    uuid = UUIDField(index=True, default=get_uuid)
    app = ForeignKeyField(App)
    date_start = DateTimeField(index=True, default=datetime.datetime.now)
    date_end = DateTimeField(default=datetime.datetime.now)
    messages_count = IntegerField(default=0)

    def add_message(self, payload):
        now = datetime.datetime.now()

        self.date_end = now
        self.messages_count += 1
        self.save()

        time_since_connection = (now - self.date_start).total_seconds()
        print(time_since_connection)

        added = 0
        for content in payload:
            added += 1
            Payload.create(
                connection=self,
                time_since_connection=time_since_connection,
                key=content["key"],
                value=content["value"]
            )

        return added


class ConnectionInfo(BaseModel):
    connection = ForeignKeyField(Connection)
    host = TextField()
    user_agent = TextField()
    accept_lang = TextField()
    ip_address = TextField()


class Payload(BaseModel):
    connection = ForeignKeyField(Connection)
    time_since_connection = FloatField()
    key = TextField(null=True)
    value = TextField(null=True)


class Metadata(BaseModel):
    version = CharField(default="0.2")

