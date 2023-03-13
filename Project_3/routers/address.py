from fastapi import Depends, APIRouter
from misc.database import get_db
from models import schema
from models.pymodels import Address
from sqlalchemy.orm import Session
from .auth import get_current_user,get_user_exception,get_password_hash,verify_password

router = APIRouter(
    prefix="/address",
    tags=["address"],
    responses= {404:{"description":"Not Found"}}
) 


@router.post("/")
async def create_address(address: Address,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    address_model = schema.Address()
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.zipcode = address.zipcode
    address_model.apt_num = address.apt_num # assignment part
    db.add(address_model)
    db.flush()

    user_model =db.query(schema.Users).filter(schema.Users.id==user.get('id')).first()

    user_model.address_id = address_model.id
    db.add(user_model)
    db.commit()
    return "ADDRESS ADDED SUCCESSFULL"