import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('flask_journal.db')


class User(UserMixin, Model):
    username = CharField(max_length=20, unique=True)
    email = CharField(max_length=100)
    password = CharField(max_length=15)
    joined_on = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        db = DATABASE
        order_by = ('-joined_on',)

    @classmethod
    def create_user(cls, username, email, password, is_admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=is_admin
                )
        except IntegrityError:
            raise ValueError("User already exists")


class Entry(Model):
    user = ForeignKeyField(rel_model=User, related_name='entries')
    title = CharField()
    content = TextField()
    date = DateTimeField(default=datetime.datetime.now)
    resources = CharField()
    time_spent = IntegerField()
    tags = CharField()

    class Meta:
        db = DATABASE
        order_by = ('-date',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry], safe=True)
    DATABASE.close()
