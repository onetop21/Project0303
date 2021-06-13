from fastapi import HTTPException

class FailAuthentcateError(HTTPException):
    def __init__(self, message='Failed to Authenticate.'):
        super().__init__(detail=message, status_code=401)

class NotFoundError(HTTPException):
    def __init__(self, message):
        super().__init__(detail=message, status_code=404)

class NotAllowedError(HTTPException):
    def __init__(self, message='Not allowed method.'):
        super().__init__(detail=message, status_code=405)
