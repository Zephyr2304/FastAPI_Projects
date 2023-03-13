from pydantic import BaseModel,Field
from typing import Optional



#This is the pydantic model for creating a new todo for user
class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="The priority must be between 1-5")
    complete: bool


#This is the pydantic model for creating a new user
class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    phone_number: Optional[str] # assignment part


#This is the pydantic model for user address
class Address(BaseModel):
    address1: str
    address2: str
    city: str
    state:str
    country:str
    zipcode:str
    apt_num: Optional[int] # assignment part

#This is the pydantic model for user verification for assignment purpose
class UserVerification(BaseModel):
    username: str
    password: str
    New_password: str