from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from fastapi import APIRouter
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from models.security.user_login import UserLogin
from models.security.user_in_db import UserInDB
from models.security.token import Token
from models.security.token_data import TokenData
# from models.security.user_signup import UserSignup


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johndoe@gmail.com": {
        "userid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "email": "johndoe@gmail.com",
        "password": "johndoe",
        "last_login": "2025-04-02T13:41:10.937Z",
        "failed_login_attempts": 0,
        "last_failed_login": "2025-04-02T13:41:10.937Z",
        "is_account_locked": False,
        "hashed_password": "$2b$12$UTO.XYQV8hSAvytgFlGVeuNI6bn9FijjUSH/JsUSgqWVQH2/RLBe6",
    }
    
    
}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, email: str):
    if email in db:
        user_dict = db[email]
        print("User found in db",user_dict)
        return UserInDB(**user_dict)

def authenticate_user(fake_db, email: str, password: str):
    user = get_user(fake_db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    print("User authenticated",user)
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    print("Creating access token",data)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user_login(token: str = Depends(oauth2_scheme)) -> UserLogin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        user = get_user(fake_users_db, email=token_data.email)
        if user is None:
            raise credentials_exception

        return user
    
    except InvalidTokenError:    
        raise credentials_exception
    
async def login_for_access_token(userlogin: UserLogin) -> Token:
    
    print(userlogin,type(userlogin))

    user = authenticate_user(fake_users_db, userlogin.email, userlogin.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")




# async def signup_user(usersignup: UserSignup) -> dict:
#     print(usersignup)
#     usersignup.created_at = datetime.now(timezone.utc)
#     get_all_users()
#     return {"message":"User signed up"}