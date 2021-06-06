from typing import Any
from pydantic import BaseModel, Field

class AlbumModel(BaseModel):
    _id: str = Field(...)
    owner: str = Field(...)
    name: str = Field(...)

class CreateModel(BaseModel):
    album_name: str = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "album_name": "new-name",
            }
        }