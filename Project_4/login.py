from datetime import timedelta
from fastapi import APIRouter, Form, HTTPException,Request,Depends,Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette import status
from sqlalchemy.orm import Session
from typing import Optional   

import sys
# adding Project_3 to the system path
sys.path.insert(0,'D:\dev-env\FastAPI\Project_3')
from misc.database import get_db
from models import schema
from routers import auth




router = APIRouter()
templates = Jinja2Templates(directory='templates')
router.mount('/static', StaticFiles(directory='static'),name="static")



class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")


@router.get("/login", response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return False
    token_expires = timedelta(minutes=60)
    token = auth.create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)

    response.set_cookie(key="access_token", value=token, httponly=True)
    return True


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token(response=response, form_data=form, db=db)

        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        return response
    except HTTPException:
        msg = "Unknown Error"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.get("/logout")
async def logout(request: Request):
    msg = "Logout Successful"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register_user(request: Request, email: str = Form(), username: str = Form(),
                        firstname: str = Form(), lastname: str = Form(),
                        password: str = Form(), password2: str = Form(),
                        db: Session = Depends(get_db)):
    validation1 = db.query(schema.Users).filter(schema.Users.username == username).first()
    validation2 = db.query(schema.Users).filter(schema.Users.email == email).first()

    if password != password2 or validation1 is not None or validation2 is not None:
        msg = "Invalid registration request"
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})

    user_model = schema.Users()
    user_model.username = username
    user_model.email = email
    user_model.first_name = firstname
    user_model.last_name = lastname

    hash_password = auth.get_password_hash(password)
    user_model.hashed_password = hash_password
    user_model.is_active = True

    db.add(user_model)
    db.commit()

    msg = "User successfully created"
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})






#--------------------------------------------------
#ASSIGNMENT PART

@router.get("/edit-password", response_class=HTMLResponse)
async def edit_user_password(request: Request):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("edit-password.html", {"request": request, "user": user})



@router.post("/edit-password", response_class=HTMLResponse)
async def register_user(request: Request,username: str = Form(),
                        password: str = Form(), password2: str = Form(),
                        db: Session = Depends(get_db)):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    user_data = db.query(schema.Users).filter(schema.Users.username == username).first()

    msg = "Invalid username or Password"
    if user_data is not None:
        if username == user_data.username and auth.verify_password(password,user_data.hashed_password):
            user_data.hashed_password = auth.get_password_hash(password2)
            db.add(user_data)
            db.commit()
            msg = "Password Updated"

    return templates.TemplateResponse("edit-password.html", {"request": request,"user": user ,"msg": msg})

