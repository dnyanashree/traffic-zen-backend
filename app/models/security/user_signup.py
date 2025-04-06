from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import datetime
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str



    @field_validator('password', mode ='after')
    @classmethod
    def modify_password(cls,value):
        return pwd_context.hash(value)