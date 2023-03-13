from sqlalchemy import Boolean,Integer,String,Column,ForeignKey
from misc.database import Base
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
    phone_no = Column(String) # assignment part
    address_id = Column(Integer,ForeignKey("address.id"),nullable=True)

    todo = relationship("Todos", back_populates="owner")
    address = relationship("Address", back_populates="user_address")


class Address(Base):

    __tablename__ = "address"
    
    id = Column(Integer,primary_key=True,index=True)
    address1 = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    zipcode = Column(String)
    apt_num = Column(Integer) # assignment part
    user_address = relationship("Users", back_populates="address")
