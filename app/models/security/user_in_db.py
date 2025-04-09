from pydantic import BaseModel, Field
from models.security.user_login import UserLogin
import uuid
from datetime import datetime

class UserInDB(UserLogin):   
    userid: uuid.UUID = Field(default=uuid.uuid4())
    hashed_password: str
    last_login: datetime | None = None
    failed_login_attempts: int | None = None
    last_failed_login: datetime | None = None
    is_account_locked: bool | None = False



