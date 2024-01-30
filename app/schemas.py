from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint



class UserOut(BaseModel):
    email: EmailStr
    id : int
    created_at: datetime
    
    class Config:
        from_attributes = True
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class CreatePost(PostBase):
    pass
class Post(PostBase):
    id: int
    owner_id : int
    created_at: datetime
    user: UserOut
    class Config:
        from_attributes = True # this is need so pydantic will read sql alchemy model
        
class PostOut(BaseModel):
    post: Post
    votes: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    username : EmailStr
    password: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(ge =0,le=1)