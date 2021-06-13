import sys
import jwt
import bcrypt
from typing import List
from fastapi import Depends, Query, Header, HTTPException
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from bson.objectid import ObjectId
from authorize import Verifier, get_router, create_token, hash_password, user_token
from models.album import CreateAlbumModel, AlbumModel, PhotoModel
from libs import datamanager as dm
from libs import exception

router = get_router()
admin_router = get_router('admin')
user_router = get_router('user')
tags = ["Album"]

# 앨범 목록
@user_router.get('/album', tags=tags)
async def get_albums(user_token=user_token('user')):
    user_info = await dm.get_user(user_token['username'])
    ret = await dm.get_albums(user_info['_id'])
    return JSONResponse(jsonable_encoder([AlbumModel(**_) for _ in ret]), 200)

# 앨범 생성
@user_router.post('/album', tags=tags)
async def create_album(album_info: CreateAlbumModel, user_token=user_token('user')):
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
async def get_photos(album_id: str):
    ret = await dm.get_photos(ObjectId(album_id))
    return JSONResponse(jsonable_encoder([PhotoModel(**_) for _ in ret]), 200)

# 사진 추가(업로드)
@user_router.post('/album/{album_id}/photo', tags=tags)
async def add_photo(album_id: str, file: UploadFile = File(...)):
    content = await file.read()
    ret = await dm.add_photo(ObjectId(album_id), file.filename, content)
    return JSONResponse({'message': 'Succeed to add photo.'}, 200)

# 사진 가져오기
@user_router.get('/album/{album_id}/photo/{photo_id}', tags=tags)
async def get_photo():
    ret = await dm.get_photos(ObjectId(album_id))
    print(ret)
    return ret

# 사진 삭제
@user_router.delete('/album/{album_id}/photo/{photo_id}', tags=tags)
async def remove_photo():
    ret = await dm.del_photo(ObjectId(photo_id))
    print(ret)
    return ret

# 앨범 삭제
@user_router.delete('/album/{album_id}', tags=tags)
async def remove_album(album_id: str, user_token=user_token('user')):
    ret = await dm.del_album(ObjectId(album_id))
    if ret.deleted_count > 0:
        return JSONResponse({'message': 'Deleted.'}, 200)
    else:
        raise exception.NotFoundError('Cannot find album.')
