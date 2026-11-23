from typing import Annotated

from fastapi import FastAPI
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
