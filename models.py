import datetime
import uuid

from peewee import Model, CharField, DateTimeField, UUIDField, IntegerField, ForeignKeyField, fn

from app import app, db


class BaseModel(Model):
    class Meta:
        database = db

def get_uuid():
    return uuid.uuid4().hex


class App(BaseModel):
    token = UUIDField(primary_key=True, default=get_uuid)
    name = CharField(unique=True)


class Connection(BaseModel):
    uuid = UUIDField(primary_key=True, default=get_uuid)
    app = ForeignKeyField(App)
    date_start = DateTimeField(default=datetime.datetime.now)
    date_end = DateTimeField(default=datetime.datetime.now)

    def add_message(self, payload):
        message = Message.create(connection=self)

        self.date_end = message.date
        self.save()

        added = 0
        for content in payload:
            added += 1
            Payload.create(message=message, key=content["key"], value=content["value"])

        return added


class ConnectionInfo(BaseModel):
    connection = ForeignKeyField(Connection)
    host = CharField()
    user_agent = CharField()
    accept_lang = CharField()
    ip_address = CharField()


class Message(BaseModel):
    connection = ForeignKeyField(Connection)
    date = DateTimeField(default=datetime.datetime.now)


class Payload(BaseModel):
    message = ForeignKeyField(Message)
    key = CharField(null=True)
    value = CharField()

