from typing import Any, Optional
from pydantic import BaseModel, Field
    
class DBSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]
    role: Optional[str]
    allow: Optional[bool]

class SignUpModel(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "username": "John Doe",
                "password": "abcdefg"
            }
        }

class SignInModel(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "username": "John Doe",
                "password": "abcdefg"
            }
        }

class InfoModel(BaseModel):
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

class UpdateModel:
    class Admin(BaseModel):
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

    class User(BaseModel):
        password: Optional[str]
        class Config:
            schema_extra = {
                "example": {
                    "password": "abcdefg",
                }
            }

