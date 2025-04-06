from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class UserLogin(BaseModel):
    userid: uuid.UUID = Field(default=uuid.uuid4())
    email: str
    password: str
    last_login: datetime | None = None
    failed_login_attempts: int | None = None
    last_failed_login: datetime | None = None
    is_account_locked: bool | None = False

