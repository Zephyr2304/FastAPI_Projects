from fastapi import FastAPI
import todo,login
from misc.database import engine
from models import schema



app = FastAPI(
    title="Project_4",
    description="This is the Full Stack todo application with frontend extension of third project",
    docs_url="/docs",
    redoc_url="/redoc")


# This line will create the database file 
schema.Base.metadata.create_all(bind=engine)

app.include_router(login.router)
app.include_router(todo.router)

