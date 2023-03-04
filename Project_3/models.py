from sqlalchemy import Boolean,Integer,String,Column
from database import Base

#This is the schema for todo app which inherit Base class,name="todos", has 5 columns.
class Todos(Base):
    
    __tablename__ = "todos"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)