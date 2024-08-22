from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: "UserRead"


class PostOut(BaseModel):
    Post: Post
    votes: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class Vote(BaseModel):
    post_id: int
    direction: int
