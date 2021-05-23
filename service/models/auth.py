from typing import Any
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

