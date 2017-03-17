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


class Connection(BaseModel):
    uuid = UUIDField(default=get_uuid)
    app = ForeignKeyField(App)
    date_start = DateTimeField(default=datetime.datetime.now)
    date_end = DateTimeField(default=datetime.datetime.now)

    def add_message(self, payload):
        now = datetime.datetime.now()
        message = Message.create(
            connection=self,
            time_since_connection = (now - self.date_start).total_seconds(),
        )

        self.date_end = now
        self.save()

        added = 0
        for content in payload:
            added += 1
            Payload.create(message=message, key=content["key"], value=content["value"])

        return added


class ConnectionInfo(BaseModel):
    connection = ForeignKeyField(Connection)
    host = TextField()
    user_agent = TextField()
    accept_lang = TextField()
    ip_address = TextField()


class Message(BaseModel):
    connection = ForeignKeyField(Connection, index=False)
    time_since_connection = FloatField()


class Payload(BaseModel):
    message = ForeignKeyField(Message, index=False)
    key = TextField(null=True)
    value = TextField()


class Metadata(BaseModel):
    version = CharField(default="0.2")

