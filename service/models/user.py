from typing import Any, Optional
from pydantic import BaseModel

class BaseUser(BaseModel):
    username: Optional[str]
    password: Optional[str]

class SignUp(BaseUser):
    pass

class SignIn(BaseUser):
    pass
    
class UserInfo(BaseUser):
    role: Optional[str]
    allow: Optional[bool]
