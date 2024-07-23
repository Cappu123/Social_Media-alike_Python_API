"""importing all the necessary modules and libraries"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint



class PostBase(BaseModel):
   """Schema for the PostBase"""
   title: str
   content: str
   published: bool = True


   class Config:
      orm_mode = True




class PostCreate(PostBase):
   """schema for creating a post"""
   pass



class UserOut(BaseModel):
   """schema for user-create response"""
   id: int
   email: EmailStr
   created_at: datetime

   class Config:
      orm_mode: True




class PostResponse(PostBase):
   """schema for the post-create Response"""
   id: int
   created_at: datetime
   owner_id: int
   owner: UserOut


   class Config:
      orm_mode = True



class postOut(BaseModel):
   """schema for post"""
   Post: PostResponse
   votes: int

   class Config:
      orm_mode = True




class UserCreate(BaseModel):
   """to create a new user"""
   email: EmailStr
   password: str



class UserLogin(BaseModel):
   """login schema"""
   email: EmailStr
   password: str




class Token(BaseModel):
   """schema for the access_token returning"""
   access_token: str
   token_type: str




class TokenData(BaseModel):
   """schema for the token data 
   we embeded in access token"""
   id: str 




class Vote(BaseModel):
   """defines schema of the vote table"""
   post_id: int
   dir: conint(le=1)
