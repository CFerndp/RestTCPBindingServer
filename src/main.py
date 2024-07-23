import logging as Logger
import time
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pylsl import StreamInfo, StreamOutlet

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

MARKER_NAME = "GNB_P300_Marker"
START_MARKER = "Start"
STOP_MARKER = "Stop"

MARKER_LENGTH = 10

def formatStreanMSG(msg: str):
    return msg[:MARKER_LENGTH].ljust(MARKER_LENGTH).capitalize()

print ("Creating a new marker stream info...\n")
info = StreamInfo(MARKER_NAME,'Markers',MARKER_LENGTH,0,'string','myuniquesourceid23443')

print("Opening an outlet...\n")
outlet =StreamOutlet(info)

print("Ready to send data...\n")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post(mainRoute + "/start_experiment/{marker}")
def start_experiment(marker: str):
    msg = formatStreanMSG(f'{START_MARKER}-{marker}')
    Logger.info("Starting experiment " + msg )
    outlet.push_sample(msg) 
    
    return {"status": "ok"}

@app.post(mainRoute + "/record_timestamp/{marker}")
def record_timestamp(marker: str):
    Logger.info(f'Recording timestamp {marker} at {time.time()}')
    outlet.push_sample(formatStreanMSG(marker)) 
    return {"status": "ok"}

@app.post(f'{mainRoute}/stop')
def stop():
    Logger.info("Stopping experiment at " + str(time.time()))
    outlet.push_sample(formatStreanMSG(STOP_MARKER))
    return {"status": "ok"}