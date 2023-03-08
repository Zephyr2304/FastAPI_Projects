from fastapi import Depends, APIRouter
from misc.database import get_db
from models.schema import Todos
from models.pymodels import Todo
from sqlalchemy.orm import Session
from .auth import get_current_user, get_user_exception
from misc.exceptions import http_exception,successful_response


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={401:{"description":"not found"}}

)

# This line will create the database file 

#Testing endpoint
@router.get('/')
async def read_database(db:Session = Depends(get_db)):
    return db.query(Todos).all()




@router.get("/user")
async def read_all_by_user(user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get("/{todo_id}")
async def read_todo(todo_id: int,
                    user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(Todos)\
        .filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get("id"))\
        .first()
    if todo_model is not None:
        return todo_model
    raise http_exception()



@router.post("/")
async def create_todo(todo: Todo,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()

    return successful_response(201)


@router.put("/{todo_id}")
async def update_todo(todo_id: int,
                      todo: Todo,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    todo_model = db.query(Todos)\
        .filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get("id"))\
        .first()

    if todo_model is None:
        raise http_exception()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return successful_response(200)



@router.delete("/{todo_id}")
async def delete_todo(todo_id: int,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    todo_model = db.query(Todos)\
        .filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get("id"))\
        .first()

    if todo_model is None:
        raise http_exception()

    db.query(Todos)\
        .filter(Todos.id == todo_id)\
        .delete()

    db.commit()

    return successful_response(200)



