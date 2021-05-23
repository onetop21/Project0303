import sys
import jwt
import bcrypt
from typing import List
from fastapi import Depends, Query, Header, HTTPException
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from authorize import Verifier, get_router, create_token, hash_password
from models.user import SignUp, SignIn, UserInfo
from libs import datamanager as dm

admin_router = get_router('admin')
user_router = get_router('user')

# 유저 목록
@admin_router.get('/user')
async def get_users():
    result = await dm.get_users()
    return [{'username': _['username']} for _ in result]

# 유저 정보
@admin_router.get('/user/{username}')
async def get_user_info(username: str):
    result = await dm.get_user(username)
    return result

# 유저 갱신
@admin_router.put('/user/{username}')
async def update_user_info(username: str, user_info: UserInfo):
    if user_info.password:
        await dm.change_password(username, hash_password(user_info.password))
    if user_info.allow != None:
        await dm.allow_user(username, user_info.allow)
    return JSONResponse('Updated.', 200)

# 탈퇴
@admin_router.delete('/user/{username}')
async def leave(username: str):
    result = await dm.del_user(username)
    return JSONResponse('Deleted.', 200)

# 본인 정보
@user_router.get('/user/me')
async def get_my_info(user_token=Depends(Verifier('user').verify)):
    return JSONResponse(user_token, 200)

# 본인 정보 갱신
@user_router.put('/user/me')
async def update_my_info(user_info: UserInfo, user_token=Depends(Verifier('user').verify)):
    if user_info.password:
        await dm.change_password(user_token['username'], hash_password(user_info.password))
    if user_info.allow != None:
        await dm.allow_user(user_token['username'], user_info.allow)
    return JSONResponse('Updated.', 200)

# 탈퇴
@user_router.delete('/user/me')
async def leave(user_token=Depends(Verifier('user').verify)):
    result = await dm.del_user(user_token['username'])
    return JSONResponse('Deleted.', 200)


