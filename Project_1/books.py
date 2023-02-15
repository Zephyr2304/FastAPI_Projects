from typing import Optional
from fastapi import FastAPI
from enum import Enum



app = FastAPI(
    title="Project_1",
    description="This is the application for basic CRUD operations",
    docs_url="/docs",
    redoc_url="/redoc")


class DirectionName(str,Enum):
    north = "north"
    south = "south"
    east = "east"
    west = "west"


@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return{"Direction": direction_name,"sub":"UP"}
    if direction_name == DirectionName.south:
        return{"Direction": direction_name,"sub":"DOWN"}
    if direction_name == DirectionName.west:
        return{"Direction": direction_name,"sub":"LEFT"}   
    return{"Direction": direction_name,"sub":"RIGHT"}


Books = {
    "book_1":{'title':'Title One', 'author':'Author One'},
    "book_2":{'title':'Title Two', 'author':'Author Two'},
    "book_3":{'title':'Title Three', 'author':'Author Three'},
    "book_4":{'title':'Title Four', 'author':'Author Four'},
    "book_5":{'title':'Title Five', 'author':'Author Five'}
}


@app.get("/")
async def get_all_books():
    return Books

@app.get("/skip")
async def skip_book(skip_book:Optional[str] =None):
    if skip_book:
        newbook = Books.copy()
        del newbook[skip_book]
        return newbook
    return Books        

@app.get("/books/{book_id}")
async def get_book(book_id:int):
    return {"Book_title":book_id}

@app.get("/{book_name}")
async def read_book(book_name:str):
    return Books[book_name]

@app.post("/")
async def create_book(book_title:str,book_author:str):
    current_book_id = 0
    if len(Books)>0:
        for book in Books:
            x = int(book.split("_")[-1])
            if x > current_book_id:
                current_book_id = x+1
    Books[f"book_{current_book_id}"] = {'title':book_title,'author':book_author}
    return Books


@app.put("/{book_name}")
async def update_book(book_name:str,book_title: str,book_author:str):
    book_information = {'title':book_title,'author':book_author}
    Books[book_name] = book_information
    return book_information

@app.delete("/{book_name}")
async def delete_book(book_name):
    del Books[book_name]
    return f"Book {book_name} deleted"


#--------------------------------------------------


# ASSIGNMENT QUESTIONS 

# 1. Create a new read book function that uses query params instead of path params.
# 2. Create a new delete book function that uses query params instead of path params.

@app.get("/assignment/")
async def read_book(book_name:str):
    return Books[book_name]

@app.delete("/assignment/")
async def delete_book(book_name):
    del Books[book_name]
    return f"Book {book_name} deleted"

#--------------------------------------------------
