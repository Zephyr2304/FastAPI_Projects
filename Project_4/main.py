from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

import sys
# adding Project_3 to the system path
sys.path.insert(0,'D:\dev-env\FastAPI\Project_3')
from misc.database import engine
from models import schema
from routers import auth, todos, users


app = FastAPI(
    title="Project_4",
    description="This is the Full Stack todo application with frontend extension of third project",
    docs_url="/docs",
    redoc_url="/redoc")


# This line will create the database file 
schema.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory='templates')


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)


@app.get("/test")
async def test(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})
