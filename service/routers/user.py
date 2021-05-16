import sys
import jwt
import bcrypt
from typing import List
from fastapi import APIRouter, Depends, Query, Header, HTTPException
from passlib.context import CryptContext

from models.user import SignUp, SignIn
from libs import datamanager as dm

router = APIRouter()

SECRET = "THISISMYSECRET!!"
passwordContext = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

# 인증 (로그인)
@router.get('/auth')
async def login():
    pass

# 유저 목록
@router.get('/user')
async def get_users():
    result = await dm.get_users()
    return [{'username': _['username']} for _ in result]

# 가입
@router.post('/user')
async def signup(user: SignUp):
    hashed_password = passwordContext.hash(user.password)
    # Add to Database
    result = await dm.add_user(user.username, hashed_password)
    return {'message': 'Succeed to signup.'}

# 유저 정보
@router.get('/user/{username}')
async def get_user(username: str):
    result = await dm.get_user(username)
    return result

# 유저 갱신
@router.put('/user/{username}')
async def update_user(username: str):
    pass

# 탈퇴
@router.delete('/user/{username}')
async def leave(username: str):
    pass


