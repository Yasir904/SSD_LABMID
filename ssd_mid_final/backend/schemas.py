from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class FileBase(BaseModel):
    filename: str
    uploaded_by: int
    shared_with: int

class FileCreate(FileBase):
    pass

class File(FileBase):
    id: int
    upload_time: datetime
    class Config:
        orm_mode = True

