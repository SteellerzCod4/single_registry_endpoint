from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserSignIn(BaseModel):
    login: str
    password: str

class UserSignUp(BaseModel):
    login: str
    password: str
    email: EmailStr
    username: str

class UserResponse(BaseModel):
    id: int
    login: str
    username: str
    email: EmailStr

