from fastapi import FastAPI
from misc.database import engine
from models import schema
from routers import auth, todos, users,address


app = FastAPI(
    title="Project_3",
    description="This is the todo application with various features of fastapi",
    docs_url="/docs",
    redoc_url="/redoc")


# This line will create the database file 
schema.Base.metadata.create_all(bind=engine)



app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(address.router)
app.include_router(users.router) # Assignment part