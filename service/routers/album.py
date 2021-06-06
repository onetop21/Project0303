import sys
import jwt
import bcrypt
from typing import List
from fastapi import Depends, Query, Header, HTTPException
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from bson.objectid import ObjectId
from authorize import Verifier, get_router, create_token, hash_password, user_token
from models.album import CreateModel, AlbumModel
from libs import datamanager as dm

router = get_router()
admin_router = get_router('admin')
user_router = get_router('user')
tags = ["Album"]

# 앨범 목록
@user_router.get('/album', tags=tags)
async def get_albums(user_token=user_token('user')):
    user_info = await dm.get_user(user_token['username'])
    ret = await dm.get_albums(user_info['_id'])
    ret = [ AlbumModel(**_) for _ in ret ]
    print(ret)
    return JSONResponse(ret, 200)

# 앨범 생성
@user_router.post('/album', tags=tags)
async def create_album(album_info: CreateModel, user_token=user_token('user')):
    user_info = await dm.get_user(user_token['username'])
    ret = await dm.create_album(user_info['_id'], album_info.album_name)
    return JSONResponse({
        'message': "Succeed to create an album.",
        'inserted_id': str(ret.inserted_id),
    }, 200)

# 앨범 다운로드
@user_router.get('/album/{album_id}/bundle', tags=tags)
async def get_album_bundle():
    pass

# 토큰 발급
@user_router.get('/album/{album_id}/token', tags=tags)
async def get_album_token():
    pass

# 사진 목록 (Thumbnail)
@user_router.get('/album/{album_id}/photo', tags=tags)
async def get_photos():
    pass

# 사진 추가(업로드)
@user_router.post('/album/{album_id}/photo', tags=tags)
async def add_photo(album_id: str, file: UploadFile = File(...)):
    content = await file.read()
    dm.add_photo(album_id, file.filename, content)

# 사진 가져오기
@user_router.get('/album/{album_id}/photo/{photo_id}', tags=tags)
async def get_photo():
    pass

# 사진 삭제
@user_router.delete('/album/{album_id}/photo/{photo_id}', tags=tags)
async def remove_photo():
    pass

# 앨범 삭제
@user_router.delete('/album/{album_id}', tags=tags)
async def remove_album():
    pass