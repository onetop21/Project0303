import os
import uvicorn
import config
from fastapi import FastAPI, Depends, Header, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from fastapi.staticfiles import StaticFiles
from routers import auth, user, album
from libs import datamanager as dm
from authorize import get_router, Verifier

API_PREFIX = '/api/v1'

app = FastAPI(
    title=f"{config.APP_NAME} API Server",
    description=f"{config.APP_NAME} is a digital picture frame application for sharing photo with family easily.",
    version=config.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

#app.add_event_handler("startup", dm.connect)
@app.on_event('startup')
async def startup_event():
    await dm.connect(config.APP_NAME.lower(), 
        mongo_addr=f"mongodb://{os.getenv('MONGO_HOST', 'localhost')}:27017",
        s3_endpoint=f"http://{os.getenv('S3_HOST', 'localhost')}:9000")
    await dm.create_index()
    await dm.add_default_admin()

#app.add_event_handler("shutdown", dm.disconnect)
@app.on_event('shutdown')
async def shutdown_event():
    await dm.disconnect()

app.include_router(get_router(), prefix=API_PREFIX)
app.include_router(get_router('user'), prefix=API_PREFIX,
                    dependencies=[Depends(Verifier(['user', 'admin']).verify)])
app.include_router(get_router('admin'), prefix=API_PREFIX,
                    dependencies=[Depends(Verifier(['admin']).verify)])
app.mount("/", StaticFiles(directory='frontend/build/web', html=True), name="frontend")

