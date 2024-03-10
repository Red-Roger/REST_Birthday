from pydantic import BaseModel, Field, EmailStr, HttpUrl
from datetime import datetime, date
        
class ContactModel(BaseModel):
    name: str = Field(min_length=3, max_length=16)
    lastname: str = Field(min_length=3, max_length=16)
    email: EmailStr
    phone: str = Field(min_length=5, max_length=16)
    birthday: date
    additional: str = Field(max_length=100)
    
class ContactResponse(BaseModel):
    id: int = 1
    name: str
    lastname: str
    email: EmailStr
    phone: str
    birthday: date
    additional: str
    contact_date: datetime
    
    class Config:
        orm_mode = True

class UpdateModel(BaseModel):
    email: EmailStr
    phone: str = Field(min_length=5, max_length=16)
    additional: str = Field(max_length=100)
        

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"