import sys
from typing import List
from fastapi import Depends, Query, Header, HTTPException
from fastapi.responses import JSONResponse
from authorize import get_router, create_token, hash_password, verify_password
from models.user import SignUp, SignIn, UserInfo
from libs import datamanager as dm

router = get_router()

# 인증 (로그인)
@router.post('/signin')
async def login(user: SignIn):
    result = await dm.get_user(user.username)
    if result:
        is_verified = verify_password(user.password, result['password'])
        if not is_verified:
            return JSONResponse(status_code=401, content=dict(message="Failed to authenticate."))
        user_info = UserInfo(**result)
        #user_info.username = result['username']
        #user_info.password = result['password']
        #user_info.role = result['role']
        #user_info.allow = result['allow']
        return {'Authorization': f"Bearer {create_token(user_info)}"}
    else:
        return JSONResponse(status_code=404, content=dict(message="Cannot find username."))

# 가입
@router.post('/signup')
async def signup(user: SignUp):
    # Add to Database
    result = await dm.add_user(user.username, hash_password(user.password))
    return {'message': 'Succeed to signup.'}



