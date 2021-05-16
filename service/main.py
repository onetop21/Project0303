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

#app.add_event_handler("startup", dm.connect)
#app.add_event_handler("shutdown", dm.disconnect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event('startup')
async def startup_event():
    await dm.connect(config.APP_NAME, 'mongodb://localhost:27017')
    await dm.create_index()

@app.on_event('shutdown')
async def shutdown_event():
    dm.disconnect()

#user_auth = Authorization('user')
#admin_auth = Authorization('admin')

app.include_router(user.router, prefix=API_PREFIX)
                    #dependencies=[Depends(user.verify_auth)])
app.mount("/", StaticFiles(directory="frontend/build/web", html=True), name="frontend")

