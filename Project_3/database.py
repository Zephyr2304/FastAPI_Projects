from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# This is the template code to make sqlite database and session 
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine)

# This is the base which is inherited by the models(schema) created in the database
Base = declarative_base()