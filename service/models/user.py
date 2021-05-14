from typing import Any
from pydantic import BaseModel

class SignUp(BaseModel):
    username: str
    password: str

class SignIn(BaseModel):
    username: str
    password: str
