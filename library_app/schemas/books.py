from pydantic import BaseModel


class BooksInfo(BaseModel):
    title: str
    description: str
    author_id: int
    id: int


class AuthorsInfo(BaseModel):
    first_name: str
    last_name: str
    id: int


class AuthorsEdit(BaseModel):
    first_name: str
    last_name: str


class BooksEdit(BaseModel):
    title: str
    description: str
    author_id: int
