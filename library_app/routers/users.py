from fastapi import APIRouter, Depends
from ..models import Users
from ..schemas.users import UserInfo
from starlette import status
from sqlalchemy.orm import Session
from ..database import get_db
from .auth import get_current_user, get_user_exception
from fastapi.encoders import jsonable_encoder


router = APIRouter(prefix="/user", tags=["user"], responses={401: {"user": "Not found"}})


@router.get("/", response_model=UserInfo, status_code=status.HTTP_200_OK)
async def get_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    user_info = jsonable_encoder(user_model, exclude_none=True)
    return user_info
