from fastapi import FastAPI
from library_app.routers import auth, books, users

app = FastAPI()


app.include_router(auth.router)
app.include_router(books.router)
app.include_router(users.router)
