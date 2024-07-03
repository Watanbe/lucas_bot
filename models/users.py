from peewee import Model, CharField, IntegerField
from .database import database

class BaseModel(Model):
    class Meta:
        database = database


class Users(BaseModel):
    username = CharField()
    chat_id = CharField()
    password = CharField()
    payment_status = IntegerField()
    payment_checkout_uri = CharField()
    payment_id = CharField()

