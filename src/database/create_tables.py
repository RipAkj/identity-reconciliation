from src.database.db_session import db
from src.contact.models.contact import Contact

def create_tables():
    try:
        db.create_tables(
            [Contact]
        )
        db.close()
        print("created tables")
    except:
        print("Exception while creating table")
        raise
