import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.api import router as api_router
import logging
import os
from datetime import date
from decouple import config

today = str(date.today())

app = FastAPI()

origins = ["http://localhost:8005"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(
        "main:app", 
        host = f"{config('HOST_IP')}", 
        port = int(f"{config('HOST_PORT')}"), 
        log_level = f"{config('WEBSERVER_LOGGING_LEVEL')}", 
        reload = bool(f"{config('RELOAD_STATUS')}"),
        workers = int(f"{config('WORKERS_NUMBER')}")
    )