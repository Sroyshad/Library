from typing import Annotated

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

Title = Annotated[str, Field(min_length=1, max_length=100)]
Author = Annotated[str, Field(min_length=1, max_length=50)]
Year = Annotated[int, Field(ge=1000, le=2026)]
Isbn = Annotated[str, Field(pattern=r"^(?:\d{10}|\d{13})$")]
Tag = Annotated[str, Field(min_length=1, max_length=20)]
Tags = list[Tag]
#pattern=r"^(?:[1-9]|1[0-9]|20)$"

class BookBase(BaseModel):
    title: Title
    author: Author
    year: Year
    isbn: Isbn
    tags: Tags = []

class Book(BookBase):
    id: int

class BookCreate(BookBase):
    pass
class BookUpdate(BaseModel):
    title: Title | None = None
    author: Author | None = None
    year: Year | None = None
    isbn: Isbn | None = None
    tags: Tags | None = None

book_db: dict[int, Book] = {}
next_id: int = 1

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate) -> Book:
    global next_id
    new_book = Book(id=next_id, **book.model_dump())
    book_db[new_book.id] = new_book
    next_id+=1
    return new_book

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int) -> Book:
    if book_id <= 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
    return book_db[book_id]