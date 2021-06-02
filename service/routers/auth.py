import sys
from typing import List
from fastapi import Depends, Query, Header, HTTPException
from fastapi.responses import JSONResponse
from authorize import get_router, create_token, hash_password, verify_password
from models.user import SignUpModel, SignInModel, InfoModel, UpdateModel
from libs import datamanager as dm

router = get_router()
tags = ["Authentication"]

# 인증 (로그인)
@router.post('/signin', tags=tags)
async def login(user: SignInModel):
    result = await dm.get_user(user.username)
    if result:
        is_verified = verify_password(user.password, result['password'])
        if not is_verified:
            return JSONResponse(status_code=401, content=dict(message="Failed to authenticate."))
        return {'Authorization': f"Bearer {create_token(InfoModel.User(**result))}"}
    else:
        return JSONResponse(status_code=404, content=dict(message="Cannot find username."))

# 가입
@router.post('/signup', tags=tags)
async def signup(user: SignUpModel):
    # Add to Database
    result = await dm.add_user(user.username, hash_password(user.password))
    return {'message': 'Succeed to signup.'}



