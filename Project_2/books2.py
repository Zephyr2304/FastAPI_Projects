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

class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(
        None, title="description of the Book",
        max_length=100,
        min_length=1
    )

Books = []

class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey, why do you want {exception.books_to_return} "
                            f"books? You need to read more!"}
    )

@app.post("/books/login")
async def book_login(username: str = Form(), password: str = Form()):
    return {"username": username, "password": password}


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}


# THis API is to get all the book present in the booklist (IF the list is empty it will call the function to fill the list)
@app.get("/")
async def get_all_Books(books_to_show: Optional[int]= None):

    if books_to_show and books_to_show < 0:
        raise NegativeNumberException(books_to_return=books_to_show)

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
    raise raise_item_cannot_be_found_exception()

@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in Books:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()

# THis API is to post new book with type: Book class defined as pydantic model and add to book list
@app.post("/",status_code=status.HTTP_201_CREATED)
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
    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in Books:
        counter += 1
        if x.id == book_id:
            del Books[counter - 1]
            return f'ID:{book_id} deleted'
    raise raise_item_cannot_be_found_exception()

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



#--------------------------------------------------

# ASSIGNMENT QUESTIONS 
# Modify our API book_login, so that it will consume an API header, that will have a username attribute and a password attribute, and it will receive a query parameter of which book the user wants to read.
# The username submitted must be called FastAPIUser and the password submitted must be test1234!
# If both the username and password are valid, return the book located specified by the query parameter
# If either username or password is invalid, return “Invalid User”
# Call this new function after calling the  read_all_books just to make sure we have setup a fake inventory


@app.post("/Assignment/login/")
async def book_login(book_id:int ,  username: str = Header(None), password: str = Header(None)):
    if username == "FastAPIUser" and password == 'test1234':
        return Books[book_id]
    return "Invalid User"
    

#--------------------------------------------------
