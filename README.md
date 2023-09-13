# fast-api-udemy-course

To run ```library_app``` project, follow these steps:
* Create virtual environment and activate it:
```
    python3 -m venv venv
    source venv/bin/activate
```
* Install all dependencies:
```
pip3 install -r requirements.txt
```
* Create a .env file and add the required parameters:
```
APP_SECRET=<some secret>
SQLALCHEMY_DATABASE_URL=<your database URL>
ALGORITHM=<algorithm to create token (e.g., HS256)>
```
* Init alembic and upgrade the migration:
```
alembic init
alembic upgrade head
```
* Run this project:
```
uvicorn app:app --reload
```
* Open the following URL:
```
Open URL: http://127.0.0.1:8000/docs
```
* Registered account, autorize and use it.
