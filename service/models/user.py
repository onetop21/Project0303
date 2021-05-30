from typing import Any, Optional
from pydantic import BaseModel, Field
    
class DBSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]
    role: Optional[str]
    allow: Optional[bool]

class SignUpSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "username": "John Doe",
                "password": "abcdefg"
            }
        }

class SignInSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "username": "John Doe",
                "password": "abcdefg"
            }
        }

class Admin:
    class InfoSchema(BaseModel):
        username: str = Field(...)
        role: str = Field(...)
        allow: bool = Field(...)
        class Config:
            schema_extra = {
                "example": {
                    "username": "John Doe",
                    "role": "abcdefg",
                    "allow": True
                }
            }

    class UpdateSchema(BaseModel):
        password: Optional[str]
        role: Optional[str]
        allow: Optional[bool]
        class Config:
            schema_extra = {
                "example": {
                    "password": "abcdefg",
                    "role": "admin",
                    "allow": True
                }
            }

class User:
    class InfoSchema(BaseModel):
        username: str = Field(...)
        role: str = Field(...)
        class Config:
            schema_extra = {
                "example": {
                    "username": "John Doe",
                    "role": "abcdefg",
                }
            }

    class UpdateSchema(BaseModel):
        password: Optional[str]
        class Config:
            schema_extra = {
                "example": {
                    "password": "abcdefg",
                }
            }

