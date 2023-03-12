import contextlib
from models import schema
from misc.database import engine
from sqlalchemy.orm import Session


@contextlib.contextmanager
def get_session():
    session = Session(bind=engine)

    try:
        yield session
        session.flush()
        session.commit()
    except Exception as e:
        print("*" * 100)
        print(e)
        print("*" * 100)
        session.rollback()
    finally:
        session.close()



# with get_session() as session:
#     session.add(schema.Users(user_name="system"))
#     session.add(schema.Users(user_name="sapradhan@levi.com"))

    session.bulk_insert_mappings(
        schema.Users,
        [
            {
                "email": "testing1@gmail.com",
                "username": "tester1",
                "first_name":"lmao",
                "last_name":"xd",
                "hashed_password":"MPOG",
            },
            {
                "email": "testing2@gmail.com",
                "username": "tester2",
                "first_name":"lol",
                "last_name":"xd",
                "hashed_password":"MPOGG",
            },
        ],
    )
    session.flush()

# with get_session() as session:
    session.bulk_insert_mappings(
        schema.Todos,
        [
            {
                "title": "Clean_up",
                "description": "Read Write Access to / endpoint",
                "priority": 3,
                "complete": False,
                "owner_id":1,
            },
            {
                "title": "Clean_up",
                "description": "Read Write Access to / endpoint",
                "priority": 1,
                "complete": False,
                "owner_id":1,
            },
            {
                "title": "Clean_up",
                "description": "Read Write Access to / endpoint",
                "priority": 5,
                "complete": False,
                "owner_id":1,
            },
            {
                "title": "Clean_up",
                "description": "Read Write Access to / endpoint",
                "priority": 4,
                "complete": False,
                "owner_id":1,
            },
            {
                "title": "Clean_up",
                "description": "Read Write Access to / endpoint",
                "priority": 3,
                "complete": False,
                "owner_id":1,
            },
        ],
    )
    session.flush()



