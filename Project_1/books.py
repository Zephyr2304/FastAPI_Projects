from fastapi import FastAPI
from enum import Enum



app = FastAPI()

Books = {
    "book_1":{'title':'Title One', 'author':'Author One'},
    "book_2":{'title':'Title Two', 'author':'Author Two'},
    "book_3":{'title':'Title Three', 'author':'Author Three'},
    "book_4":{'title':'Title Four', 'author':'Author Four'},
    "book_5":{'title':'Title Five', 'author':'Author Five'}
}

class DirectionName(str,Enum):
    north = "north"
    south = "south"
    east = "east"
    west = "west"

@app.get("/")
async def get_all_books():
    return Books

@app.get("/books/{book_id}")
async def get_book(book_id:int):
    return {"Book_title":book_id}

@app.get("/{book_name}")
async def read_book(book_name:str):
    return Books[book_name]




@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return{"Direction": direction_name,"sub":"UP"}
    if direction_name == DirectionName.south:
        return{"Direction": direction_name,"sub":"DOWN"}
    if direction_name == DirectionName.west:
        return{"Direction": direction_name,"sub":"LEFT"}   
    return{"Direction": direction_name,"sub":"RIGHT"}