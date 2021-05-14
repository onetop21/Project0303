import boto3
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

client: AsyncIOMotorClient = None
db = None

async def connect():
    global client, db
    if not client:
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        db = client['project0303']

async def disconnect():
    global client, db
    if client:
        client.close()
        client = None
        db = None

# User
async def get_users():
    result = []
    async for doc in db.user.find():
        result.append(doc)
    return result

async def add_user(username: str, password: str):
    result = await db.user.insert_one(
        {'username': username, 'password': password, 'allow': False}
    )
    return result

async def get_user(username: str):
    result = await db.user.find_one(
        {'username': username}
    )
    return result

async def allow_user(username: str, allow: bool=True):
    result = await db.user.update_one(
        {'username': username}, 
        {'$set': {'allow': allow}}
    )
    return result

async def change_password(username: str, password: str):
    result = await db.user.update_one(
        {'username': username},
        {'$set': {'password': password}}
    )
    return result

async def del_user(username: str):
    result = await db.user.delete_one(
        {'username': username}
    )
    return result

# Album
async def get_albums(user_id: ObjectId):
    result = await db.album.find(
        {'owner': user_id}
    )
    return result

async def create_album(user_id: ObjectId, name: str):
    result = await db.album.insert_one(
        {'name': name, 'owner': user_id}
    )
    return result

async def get_album(id: ObjectId):
    result = await db.album.find_one(
        {'_id': id}
    )
    return result

async def del_album(id: ObjectId):
    result = await db.album.delete_one(
        {'_id': id}
    )
    return result

# Photo
async def get_photos(album_id: ObjectId):
    result = await db.photo.find(
        {'owner': album_id}
    )
    return result

async def get_photo(id: ObjectId):
    result = await db.photo.find_one(
        {'_id': id}
    )
    return result
