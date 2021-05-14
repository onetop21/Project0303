from service.libs.auth import verify_token, decode_token
from fastapi import HTTPException, Header

class Authorization():
    def __init__(self, role):
        self.role = role #role for API

    async def verify_auth(self, token:str=Header(...)):
        try:
            decoded = decode_token(token)
        except Exception as e:
            raise HTTPException(status_code=401, 
                                detail=f"Unauthorized request : {e}")
        if not verify_token(decoded):
            raise HTTPException(status_code=401, 
                                detail="Unauthorized request : expired token")
        else:
            if decoded['role']=='admin':
                return True
            else:
                if self.role == "user":
                    return True
                else:
                    raise HTTPException(status_code=403, 
                                        detail="Forbidden request")
