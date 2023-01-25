from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return) -> None:
        self.books_to_return = books_to_return


app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book", max_length=100, min_length=1)
    ratting: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "7123-dsf-asda",
                "title": "Computer Science",
                "author": "Mark",
                "description": "Is a very good description",
                "rating": 75,
            }
        }


class BookNoRatting(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book", max_length=100, min_length=1)
    ratting: int = Field(gt=-1, lt=101)


BOOKS: list = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request, exception: NegativeNumberException):
    return JSONResponse(status_code=418, content={"message": f"Hey, why do you want {exception.books_to_return}"})


@app.get("/{book_id}", response_model=BookNoRatting)
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise HTTPException(
        status_code=404, detail="Book not found", headers={"X-Header-Error": "Nothing to be seen at the UUID"}
    )


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book
