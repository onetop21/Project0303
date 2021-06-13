from typing import Any
from pydantic import BaseModel, BaseConfig, Field
from bson.objectid import ObjectId

class PydanticObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)

class MongoSchema(BaseModel):
    id: PydanticObjectId = Field(..., alias='_id')
    class Config(BaseConfig):
        json_encoders = {
            PydanticObjectId: lambda x: ObjectId(x)
        }

class AlbumModel(MongoSchema):
    owner: PydanticObjectId = Field(...)
    name: str = Field(...)

class CreateAlbumModel(BaseModel):
    album_name: str = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "album_name": "new-name",
            }
        }
    
class PhotoModel(MongoSchema):
    bucket: str = Field(...)
    path: str = Field(...)
    verified: bool = Field(...)
    owner: PydanticObjectId = Field(...)
    