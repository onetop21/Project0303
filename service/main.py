import os
import uvicorn
import config
from fastapi import FastAPI, Depends, Header, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from fastapi.staticfiles import StaticFiles
#from auth import Authorization
from routers import user
from libs import datamanager as dm

API_PREFIX = '/api/v1'

app = FastAPI(
    title=f"{config.APP_NAME} API Server",
    description=f"{config.APP_NAME} is a digital picture frame application for sharing photo with family easily.",
    version=config.VERSION,
)

app.add_event_handler("startup", dm.connect)
app.add_event_handler("shutdown", dm.disconnect)

app.mount("/", StaticFiles(directory="frontend/build/web", html=True), name="frontend")
#@app.get('/')
#async def home(request: Request):
#    print('Hello?')
#    return FileResponse('frontend/build/web/index.html', media_type='text/html')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

#user_auth = Authorization('user')
#admin_auth = Authorization('admin')

app.include_router(user.router, prefix=API_PREFIX)
                    #dependencies=[Depends(user.verify_auth)])
