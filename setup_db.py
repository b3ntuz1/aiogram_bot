# db.py
import os
import psycopg2
from peewee import *
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL'))
# db = SqliteDatabase("data.db")

class BaseModel(Model):
	class Meta:
		database = db

class KVStorage(BaseModel):
	key = CharField()
	value = CharField()

	class Meta:
		db_table = "kv_storage"

if not KVStorage.table_exists():
	print("Table not exists")
	KVStorage.create_table()
