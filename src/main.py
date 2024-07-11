import logging as Logger
import time
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import socket

TCP_HOST = "127.0.0.1"
TCP_PORT = 1234


app = FastAPI()

mainRoute = "/enobio_binding"

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows the origins listed in the `origins` list
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


Logger.basicConfig(level=Logger.INFO)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((TCP_HOST, TCP_PORT))
    

    @app.get("/")
    def read_root():
        return {"Hello": "World"}


    @app.post(f'{mainRoute}/start_experiment')
    def start_experiment():
        Logger.info("Starting experiment")
        s.sendall(b"start_experiment")
        return {"status": "ok"}

    @app.post(f'{mainRoute}/record_timestamp')
    def record_timestamp():
        s.sendall(b"RECORD MTF")
        Logger.info("Record Timestamp at " + str(time.time()))
        return {"status": "ok"}

    @app.post(f'{mainRoute}/stop')
    def stop():
        s.sendall(b"STOP")
        Logger.info("Stopping experiment at " + str(time.time()))
        return {"status": "ok"}