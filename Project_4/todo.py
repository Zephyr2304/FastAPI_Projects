from fastapi import APIRouter, Form, Request,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette import status
from sqlalchemy.orm import Session
from typing import Optional   

import sys
# adding Project_3 to the system path
sys.path.insert(0,'D:\dev-env\FastAPI\Project_3')
from misc.database import engine, get_db
from models import schema
from routers import auth


router = APIRouter()


templates = Jinja2Templates(directory='templates')
router.mount('/static', StaticFiles(directory='static'),name="static")




@router.get("/todos", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):

    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    todos = db.query(schema.Todos).filter(schema.Todos.owner_id == user.get("id")).all()

    return templates.TemplateResponse("home.html", {"request": request, "todos": todos, "user": user})

@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})

@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(), description: str = Form(),
                      priority: int = Form(), db: Session = Depends(get_db)):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    todo_model = schema.Todos()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.complete = False
    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):

    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    todo = db.query(schema.Todos).filter(schema.Todos.id == todo_id).first()

    return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})


@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_commit(request: Request, todo_id: int, title: str = Form(),
                           description: str = Form(), priority: int = Form(),
                           db: Session = Depends(get_db)):

    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    todo_model = db.query(schema.Todos).filter(schema.Todos.id == todo_id).first()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority

    db.add(todo_model)
    db.commit()
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/delete/{todo_id}")
async def delete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = await auth.get_current_user(request)

    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    todo_model = db.query(schema.Todos).filter(schema.Todos.id == todo_id).filter(
        schema.Todos.owner_id == user.get("id")).first()
    if todo_model is None:
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
    
    db.query(schema.Todos).filter(schema.Todos.id == todo_id).delete()
    db.commit()
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/complete/{todo_id}", response_class=HTMLResponse)
async def complete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):

    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    todo = db.query(schema.Todos).filter(schema.Todos.id == todo_id).first()

    todo.complete = not todo.complete

    db.add(todo)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
