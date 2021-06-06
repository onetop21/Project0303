import jwt
from typing import List, Optional
from fastapi import HTTPException, Header, Depends, APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from models.user import UpdateModel, InfoModel

SECRET = "56090b7630b643b48d3beaf05e699c1c"
ALGORITHM = 'HS256'
BASE_ROLE = '__GUEST__'
passwordContext = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
security = HTTPBearer()

_router: dict = {}
def get_router(role: str=BASE_ROLE):
    global _router
    router = _router[role] = _router.get(role, APIRouter())
    return router

def create_token(user_info: InfoModel):
    return jwt.encode(user_info.dict(), SECRET, algorithm=ALGORITHM)

def hash_password(password: str):
    return passwordContext.hash(password)

def verify_password(secret: str, hash: str):
    return passwordContext.verify(secret, hash)
    return bcrypt.checkpw(secret.encode(), hash.encode())

def user_token(*args):
    return Depends(Verifier(list(args)).verify)

class Verifier:
    def __init__(self, roles: List[str]=[BASE_ROLE]):
        self._roles = roles if isinstance(roles, list) else [roles]

    async def verify(self, credentials: HTTPAuthorizationCredentials = Security(security)):
        print( {"scheme": credentials.scheme, "credentials": credentials.credentials})
        if credentials.scheme.lower() == 'bearer':
            try:
                decoded = jwt.decode(credentials.credentials, SECRET, algorithms=[ALGORITHM])
                print(decoded, self._roles)
                if decoded['allow']:
                    if decoded['role'] in self._roles:
                        return decoded
                    else:
                        raise HTTPException(401, "Role is not matched.")
                else:
                    raise HTTPException(405, "Please contact to administrator.")
            except jwt.exceptions.InvalidSignatureError as e:
                raise HTTPException(401, f"{e}")
            except jwt.exceptions.InvalidTokenError as e:
                raise HTTPException(401, f"{e}")
            except Exception as e:
                raise e
        else:
            raise HTTPException(401, "Invalid token scheme.")
        

