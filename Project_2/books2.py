from typing import Optional
from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from uuid import UUID


app = FastAPI(
    title="Project_2",
    description="This is the application build on top of project_1 with further features and explorations",
    docs_url="/docs",
    redoc_url="/redoc")

class Book(BaseModel):
    id:UUID
    title:str
    author:str
    description: str
    rating:int

Books = []

@app.get("/")
async def get_all_books():
    return Books



@app.post("/")

async def create_book(book:Book):
    Books.append(book)
    return Books