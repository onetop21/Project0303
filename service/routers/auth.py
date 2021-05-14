from typing import List
from fastapi import APIRouter, Query, Header, HTTPException
from project0303.service.models.auth import TokenRequest
from project0303.service.libs.auth import generate_user_token
from project0303.service.libs.auth import decode_token, verify_token

admin_router = APIRouter()
user_router = APIRouter()

import bcrypt
import jwp

@admin_router.post("/auth")
def create_token(req: TokenRequest):
    username = req.username
    user_token = generate_user_token(username)
    return {'token': user_token}

@user_router.get("/user/auth")
def verify_user(user_token: str = Header(...)):
    decoded = decode_token(user_token)
    res = verify_token(decoded)
    if res:
        del decoded['hash_key']
        return {'result': res, 'data': decoded}
    else:
        return {'result': res}