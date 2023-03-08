from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# For local database
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"  

# For production database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/Todo_app"  


# This is the template code to make sqlite database and session 
# engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})

# This is the template to make postgres database and session 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine)

# This is the base which is inherited by the models(schema) created in the database
Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()