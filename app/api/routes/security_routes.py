from fastapi import APIRouter
from core.security import login_for_access_token
from models.security.user_login import UserLogin
from models.security.token import Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model=Token)
async def token(userlogin: UserLogin) -> Token:
    return await login_for_access_token(userlogin)


