from typing import Optional
from fastapi import FastAPI
from enum import Enum

app =FastAPI()


BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
}
               

class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"


@app.get("/directions/{direction_name}")
async def get_direction(directions_name: DirectionName):
    if directions_name == DirectionName.north:
        return {"Direction": directions_name, "sub": "Up"}
    if directions_name == DirectionName.south:
        return {"Direction": directions_name, "sub": "Down"}
    if directions_name == DirectionName.west:
        return {"Direction": directions_name, "sub": "Left"}
    return {"Direction": directions_name, "sub": "Right"}


@app.post("/")
async def create_book(book_title, book_author):
    current_book_id = 0

    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split('_')[-1])
            if x > current_book_id:
                current_book_id = x
    
    BOOKS[f'book_{current_book_id + 1}'] = {'title': book_title, 'author': book_author}
    return BOOKS[f'book_{current_book_id + 1}']


@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    book_information = {"title": book_title, "author": book_author}
    BOOKS[book_name] = book_information
    return book_information


@app.delete("/")
async def delete_book(book_name: Optional[str] = None):
    if book_name:
        del BOOKS[book_name]
        return f'Book_{book_name} deleted'
    return f'Choose a book: {BOOKS.keys()}'


@app.get('/')
async def read_book(book_name: Optional[str] = None):
    if book_name:
        return BOOKS[book_name]
    return BOOKS




