import sys
import jwt
import bcrypt
from typing import List
from fastapi import Depends, Query, Header, HTTPException
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from authorize import Verifier, get_router, create_token, hash_password
from models.user import SignUpModel, SignInModel, InfoModel, UpdateModel
from libs import datamanager as dm

router = get_router()
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
    if result:
        user_info = UserInfo(**result)
        return user_info.dict(exclude={'password'})
    else:
        raise HTTPException(404, "Cannot find user.")

# 유저 갱신
@admin_router.put('/user/{username}')
async def update_user_info(username: str, user_info: InfoModel.Admin):
    result = await dm.get_user(username)
    if result:
        update_properties = []
        if user_info.password:
            await dm.change_password(username, hash_password(user_info.password))
            update_properties.append('Password')
        if user_info.allow != None:
            if result['role'] != 'admin':
                await dm.allow_user(username, user_info.allow)
                update_properties.append('Allow')
            else:
                raise HTTPException(403, 'Not allowed modify allow property of admin account.')
        return JSONResponse(f'Updated {update_properties}.', 200)
    else:
        raise HTTPException(404, "Cannot find user.")

# 탈퇴
@admin_router.delete('/user/{username}')
async def leave(username: str):
    result = await dm.get_user(username)
    if result:
        if result['role'] != 'admin':
            result = await dm.del_user(username)
        else:
            raise HTTPException(403, 'Not allowed remove account of admin account.')
        return JSONResponse('Deleted.', 200)
    else:
        raise HTTPException(404, "Cannot find user.")


# 본인 정보
@router.get('/user/me')
async def get_my_info(user_token=Depends(Verifier(['user', 'admin']).verify)):
    return JSONResponse(user_token, 200)

# 본인 정보 갱신
@router.put('/user/me')
async def update_my_info(user_info: InfoModel.User, user_token=Depends(Verifier(['user', 'admin']).verify)):
    update_properties = []
    if user_info.password:
        await dm.change_password(user_token['username'], hash_password(user_info.password))
        update_properties.append('Password')
    if user_info.allow != None:
        if user_token['role'] != 'admin':
            await dm.allow_user(user_token['username'], user_info.allow)
            update_properties.append('Allow')
        else:
            raise HTTPException(403, 'Not allowed modify allow property of admin account.')
    return JSONResponse(f'Updated. {update_properties}', 200)

# 탈퇴
@router.delete('/user/me')
async def leave(user_token=Depends(Verifier(['user', 'admin']).verify)):
    if user_token['role'] != 'admin':
        result = await dm.del_user(user_token['username'])
    else:
        raise HTTPException(403, 'Not allowed remove account of admin account.')
    return JSONResponse('Deleted.', 200)


