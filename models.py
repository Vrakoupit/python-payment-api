from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('my_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    email = CharField()
    password = CharField()
    mobile = CharField()

class Token(BaseModel):
    value = CharField()
    user_id = ForeignKeyField(User, related_name='tokens')
    created_at = DateTimeField(default=datetime.datetime.now)

class Payment(BaseModel):
    created_at = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, related_name='transactions')
    amount = FloatField()
    label = TextField()

class Code(BaseModel):
    value = CharField()
    user_id = ForeignKeyField(User, related_name='codes')
    charge_id = CharField()

# create table
User.create_table(True)
Code.create_table(True)
Token.create_table(True)
Payment.create_table(True)

# connect db
db.connect()