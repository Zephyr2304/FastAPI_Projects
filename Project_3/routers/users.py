# Assignment

# Here is your opportunity to keep learning!

# Recap what we have learned. We will be creating a new route that has a lot of functionality that we have learned thus far from FastAPI :)



# Create a new route within the routers directory called users.py

# Enhance users.py to be able to return all users within the application

# Enhance users.py to be able to get a single user by a path parameter

# Enhance users.py to be able to get a single user by a query parameter

# Enhance users.py to be able to modify their current user's password, if passed by authentication

# Enhance users.py to be able to delete their own user.

from fastapi import Depends, APIRouter
from misc.database import get_db
from models.schema import Users
from models.pymodels import UserVerification
from sqlalchemy.orm import Session
from .auth import get_current_user,get_user_exception,get_password_hash,verify_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses= {404:{"description":"Not Found"}}
) 


@router.get("/")
async def read_all(db:Session = Depends(get_db)):
    return db.query(Users).all()


@router.get("/user/{user_id}")
async def user_by_path(user_id:int, db:Session=Depends(get_db)):
    user_model =db.query(Users).filter(Users.id==user_id).first()
    if user_model is not None:
        return user_model
    return "Invalid User ID"



@router.get("/user/")
async def user_by_query(user_id:int, db:Session=Depends(get_db)):
    user_model =db.query(Users).filter(Users.id==user_id).first()
    if user_model is not None:
        return user_model
    return "Invalid User ID"



@router.get("/user/{user_id}")
async def user_by_path(user_id:int, db:Session=Depends(get_db)):
    user_model =db.query(Users).filter(Users.id==user_id).first()
    if user_model is not None:
        return user_model
    return "Invalid User ID"



@router.put("/user/password")
async def user_password_change(user_verification:UserVerification,user:dict= Depends(get_current_user) ,db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user_model =db.query(Users).filter(Users.id==user.get('id')).first()
    if user is not None:
        if user_verification.username == user_model.username and verify_password(
            user_verification.password,
            user_model.hashed_password):
            user_model.hashed_password = get_password_hash(user_verification.New_password)
            db.add(user_model)
            db.commit()
            return "SUCCESSFUL"
    return "Invalid User request"


@router.delete("/user")
async def delete_user(user:dict= Depends(get_current_user) ,db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user_model =db.query(Users).filter(Users.id==user.get('id')).first()
    if user_model is None:
        return "Invalid User or request"
    db.query(Users).filter(Users.id==user.get('id')).delete()
    db.commit()
    return "User Deleted Successfully"
