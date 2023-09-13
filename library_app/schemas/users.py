from pydantic import BaseModel


class UserInfo(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
