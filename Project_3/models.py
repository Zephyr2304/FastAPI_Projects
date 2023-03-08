from sqlalchemy import Boolean,Integer,String,Column,ForeignKey
from database import Base
from sqlalchemy.orm import relationship

#This is the schema for todo app which inherit Base class,name="todos", has 5 columns.
class Todos(Base):
    
    __tablename__ = "todos"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer,ForeignKey("users.id"))

    owner = relationship("Users", back_populates="todo")


class Users(Base):

    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String, unique=True,index=True)
    username = Column(String,unique=True,index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    todo = relationship("Todos", back_populates="owner")


