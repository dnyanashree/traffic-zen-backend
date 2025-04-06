from pydantic import Field
from models.security.user_signup import UserSignup
from datetime import datetime, timezone

class UserInDBSignup(UserSignup):   
    is_active: int = 1
    created_at: datetime = Field(default = datetime.now(timezone.utc))
    verification_token: str | None = None
    verification_token_expiration: datetime | None = None