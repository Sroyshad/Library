from typing import Annotated

from fastapi import FastAPI, status, HTTPException, Path
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

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, summary="Adding a book/Добавить Книгу")
def create_book(book: BookCreate) -> Book:
    global next_id
    new_book = Book(id=next_id, **book.model_dump())
    book_db[new_book.id] = new_book
    next_id+=1
    return new_book

@app.get("/books/{book_id}", response_model=Book, summary="retrieve a book by ID/получить книгу по ID")
def read_book(book_id: Annotated[int, Path(gt=0)]) -> Book:
    if book_id not in book_db:
        raise HTTPException(status_code=404, detail=f"The book with the given <{book_id}> is missing from the database.")
    return book_db[book_id]

@app.get("/books", response_model=list[Book], summary="Return all books/Вернуть все книги")
def list_books() -> list[Book]:
    return list(book_db.values())