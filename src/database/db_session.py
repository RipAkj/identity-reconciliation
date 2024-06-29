from peewee import *
db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db = PostgresqlDatabase('postgres', host='localhost', port=5433, user='postgres', password='1234')
db.connect()

