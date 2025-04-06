from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from core.security import get_user_login
from models.security.user_login import UserLogin
from models.security.user_signup import UserSignup
from models.security.user_in_db_signup import UserInDBSignup
from db.database import add_user, check_user_exists
# from core.googleapis import send_verification_token_email

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me",response_model=UserLogin)
async def read_users_me(current_user: Annotated[UserLogin, Depends(get_user_login)]):
    if current_user.is_account_locked:
        raise HTTPException(status_code=400, detail="Account Locked!")
    return current_user

@router.post("/signup")
async def signup(usersignup: UserSignup) -> dict:

    if check_user_exists(usersignup.email):
        raise HTTPException(status_code=400, detail="Email already registered! Please login.")
    add_user(UserInDBSignup(**(usersignup.model_dump())))
    # send_verification_token_email()

    return {'message': 'User created successfully!'}