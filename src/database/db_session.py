from peewee import *
from env import *
db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db = PostgresqlDatabase(database=DATABASE_NAME, host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASSWORD)
db.connect()

