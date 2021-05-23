import boto3
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from pymongo.errors import (
    DuplicateKeyError
)
from authorize import hash_password

client: AsyncIOMotorClient = None
db = None

async def connect(name, address='mongodb://localhost:27017'):
    global client, db
    if not client:
        client = AsyncIOMotorClient(address)
        db = client[name]

async def disconnect():
    global client, db
    if client:
        client.close()
        client = None
        db = None

def mongo(fn):
    global db
    async def wrapper(*args, **kwargs):
        if not db: raise Exception('Database is not connected.')
        try:
            return await fn(*args, **kwargs)
        except DuplicateKeyError as e:
            raise HTTPException(status_code=409, detail=str(e))
    return wrapper

@mongo
async def create_index():
    collection = db.user
    result = await collection.create_index('username', unique=True)
    return result

@mongo
async def add_default_admin():
    if not await db.user.find_one({'username': 'admin'}):
        result = await db.user.insert_one(
            {'username': 'admin', 'password': hash_password(''), 'role': 'admin', 'allow': True}
        )
        print('Added default admin account. Please change password first.')
# User
@mongo
async def get_users():
    result = []
    async for doc in db.user.find():
        result.append(doc)
    return result

@mongo
async def add_user(username: str, password: str):
    result = await db.user.insert_one(
        {'username': username, 'password': password, 'role': 'user', 'allow': False}
    )
    return result

@mongo
async def get_user(username: str):
    result = await db.user.find_one(
        {'username': username}
    )
    return result

@mongo
async def allow_user(username: str, allow: bool=True):
    result = await db.user.update_one(
        {'username': username}, 
        {'$set': {'allow': allow}}
    )
    return result

@mongo
async def change_password(username: str, password: str):
    result = await db.user.update_one(
        {'username': username},
        {'$set': {'password': password}}
    )
    return result

@mongo
async def del_user(username: str):
    result = await db.user.delete_one(
        {'username': username}
    )
    return result

# Album
@mongo
async def get_albums(user_id: ObjectId):
    result = await db.album.find(
        {'owner': user_id}
    )
    return result

@mongo
async def create_album(user_id: ObjectId, name: str):
    result = await db.album.insert_one(
        {'name': name, 'owner': user_id}
    )
    return result

@mongo
async def get_album(id: ObjectId):
    result = await db.album.find_one(
        {'_id': id}
    )
    return result

@mongo
async def del_album(id: ObjectId):
    result = await db.album.delete_one(
        {'_id': id}
    )
    return result

# Photo
@mongo
async def get_photos(album_id: ObjectId):
    result = await db.photo.find(
        {'owner': album_id}
    )
    return result

@mongo
async def get_photo(id: ObjectId):
    result = await db.photo.find_one(
        {'_id': id}
    )
    return result
