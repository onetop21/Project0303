import sys
import jwt
import bcrypt
from typing import List
from fastapi import Depends, Query, Header, HTTPException
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from bson.objectid import ObjectId
from authorize import Verifier, get_router, create_token, hash_password
from models.user import SignUp, SignIn, UserInfo
from libs import datamanager as dm

router = get_router()
admin_router = get_router('admin')
user_router = get_router('user')

# 앨범 목록
@user_router.get('/album')
async def get_albums():
    pass

# 앨범 생성
@user_router.post('/album')
async def create_album():
    async dm.create_album()

# 앨범 다운로드
@user_router.get('/album/{album_id}/bundle')
async def get_album_bundle():
    pass

# 토큰 발급
@user_router.get('/album/{album_id}/token')
async def get_album_token():
    pass

# 사진 목록 (Thumbnail)
@user_router.get('/album/{album_id}/photo')
async def get_photos():
    pass

# 사진 추가(업로드)
@user_router.post('/album/{album_id}/photo')
async def add_photo(album_id: str, file: UploadFile = File(...)):
    content = await file.read()
    dm.add_photo(album_id, file.filename, content)

# 사진 가져오기
@user_router.get('/album/{album_id}/photo/{photo_id}')
async def get_photo():
    pass

# 사진 삭제
@user_router.delete('/album/{album_id}/photo/{photo_id}')
async def remove_photo():
    pass

# 앨범 삭제
@user_router.delete('/album/{album_id}')
async def remove_album():
    pass