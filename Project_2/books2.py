from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


app = FastAPI(
    title="Project_2",
    description="This is the application build on top of project_1 with further features and explorations",
    docs_url="/docs",
    redoc_url="/redoc")


# This Book Class is a response model to create book object in our api with defined attributes and Field constraints
class Book(BaseModel):
    id:UUID
    title:str =Field(min_length=1)
    author:str = Field(min_length=1,max_length=100)
    description: Optional[str] = Field(title="Description of book",
                                        min_length=1,
                                        max_length=100)
    rating:int =Field(gt=-1,lt=6)

    # This Class extends over basemodel to give a predefined Customised Schema for our Request body
    class Config:
        Predef_schema = {
            "example": {
                "id": "11f4c2ea-1340-41f4-89f7-2852347bb0d1",
                "title": "Preset schema",
                "author": "Zephyr",
                "description": "A very nice description of a book",
                "rating": 3
            }
        }


Books = []

# THis API is to get all the book present in the booklist (IF the list is empty it will call the function to fill the list)
@app.get("/")
async def get_all_Books(books_to_show: Optional[int]= None):
    if len(Books) < 1:
        Add_random_books()
    if books_to_show and len(Books) >= books_to_show > 0:
        i =1
        new_books =[]
        while i <= books_to_show:
            new_books.append(Books[i-1])
            i+=1
        return new_books
    return Books

@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in Books:
        if x.id == book_id:
            return x

# THis API is to post new book with type: Book class defined as pydantic model and add to book list
@app.post("/")
async def create_book(book:Book):
    Books.append(book)
    return Books

@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in Books:
        counter += 1
        if x.id == book_id:
            Books[counter - 1] = book
            return Books[counter - 1]


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in Books:
        counter += 1
        if x.id == book_id:
            del Books[counter - 1]
            return f'ID:{book_id} deleted'

# THis function is to add some random books so that the list should never be empty 
def Add_random_books():
    book_1 = Book(id="71f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=5)
    book_2 = Book(id="21f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=2)
    book_3 = Book(id="31f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=3)
    book_4 = Book(id="41f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=1)

    Books.append(book_1)
    Books.append(book_2)
    Books.append(book_3)
    Books.append(book_4)



def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404,
                         detail="Book not found",
                         headers={"X-Header_Error":
                                  "Nothing to be seen at the UUID"})


