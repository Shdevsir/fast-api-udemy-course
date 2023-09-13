from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .auth import get_current_user, get_user_exception
from ..models import Books, Users, Authors, user_books
from ..schemas.books import BooksInfo, AuthorsInfo, BooksEdit, AuthorsEdit
from starlette import status
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/books", tags=["books"], responses={404: {"description": "Not found"}})


@router.get("/authors", response_model=list[AuthorsInfo], status_code=status.HTTP_200_OK)
async def get_all_authors(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    authors_model = db.query(Authors).all()
    authors_info = jsonable_encoder(authors_model, exclude_none=True)
    return authors_info


@router.get("/user-books", response_model=list[BooksInfo], status_code=status.HTTP_200_OK)
async def get_all_user_books(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    books_model = (
        db.query(Books)
        .join(user_books, Books.id == user_books.c.book_id)
        .filter(user_books.c.user_id == user.get("id"))
        .all()
    )
    books_info = [
        BooksInfo(title=book.title, description=book.description, author_id=book.author_id, id=book.id)
        for book in books_model
    ]
    return books_info


@router.get("/", response_model=list[BooksInfo], status_code=status.HTTP_200_OK)
async def get_all_books(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    books_model = db.query(Books).all()
    books_info = jsonable_encoder(books_model, exclude_none=True)
    return books_info


@router.get("/{book_id}", response_model=BooksInfo, status_code=status.HTTP_200_OK)
async def get_book(book_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    book_model = db.query(Books).filter(Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(status_code=404, detail="Book is not found.")
    books_info = jsonable_encoder(book_model, exclude_none=True)
    return books_info


@router.get("/authors/{author_id}", response_model=AuthorsInfo, status_code=status.HTTP_200_OK)
async def get_author(author_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    author_model = db.query(Authors).filter(Authors.id == author_id).first()
    if author_model is None:
        raise HTTPException(status_code=404, detail="Author is not found.")
    author_info = jsonable_encoder(author_model, exclude_none=True)
    return author_info


@router.post("/", response_description="Book is created", status_code=status.HTTP_200_OK)
async def create_book(book: BooksEdit, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    author_model = db.query(Authors).filter(Authors.id == book.author_id).first()
    if author_model is None:
        raise HTTPException(status_code=404, detail="Author is not found.")
    book_model = Books()
    book_model.author_id = book.author_id
    book_model.description = book.description
    book_model.title = book.title
    db.add(book_model)
    db.commit()
    return {"message": "Book is created."}


@router.post("/authors", response_description="Author is created", status_code=status.HTTP_200_OK)
async def create_author(author: AuthorsEdit, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    author_model = Authors()
    author_model.first_name = author.first_name
    author_model.last_name = author.last_name
    db.add(author_model)
    db.commit()
    return {"message": "Author is created."}


@router.get("/user-books/{book_id}", status_code=status.HTTP_200_OK, response_description="Book is added")
async def set_book(book_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    book_model = db.query(Books).filter(Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(status_code=404, detail="Book is not found")
    user_id = user.get("id")
    user_model = db.query(Users).filter(Users.id == user_id).first()
    user_model.books.append(book_model)
    db.commit()
    return {"message": "Book is added."}


@router.delete("/{book_id}", status_code=status.HTTP_200_OK, response_description="Book is deleted")
async def delete_book(book_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    book_model = db.query(Books).filter(Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(status_code=404, detail="Book is not found")
    db.query(Books).filter(Books.id == book_id).delete()
    db.commit()
    return {"message": "Book is deleted."}


@router.delete("/authors/{author_id}", response_description="Author is deleted", status_code=status.HTTP_200_OK)
async def delete_author(author_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    author_model = db.query(Authors).filter(Authors.id == author_id).first()
    if author_model is None:
        raise HTTPException(status_code=404, detail="Author is not found")
    db.query(Authors).filter(Authors.id == author_id).delete()
    db.commit()
    return {"message": "Author is deleted."}


@router.delete(
    "/user-books/{book_id}", response_description="Book is deleted from user", status_code=status.HTTP_200_OK
)
async def delete_book_from_user(book_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    book_model = db.query(Books).filter(Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(status_code=404, detail="Book is not found")
    user_id = user.get("id")
    user_model = db.query(Users).filter(Users.id == user_id).first()
    user_model.books.remove(book_model)
    db.commit()
    return {"message": "Book is deleted from user."}
