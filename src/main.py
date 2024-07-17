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

print ("Creating a new marker stream info...\n")
info = StreamInfo(MARKER_NAME,'Markers',1,0,'int32','myuniquesourceid23443')

print("Opening an outlet...\n")
outlet =StreamOutlet(info)

print("Ready to send data...\n")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post(f'{mainRoute}/start_experiment')
def start_experiment():
    Logger.info("Starting experiment")
    outlet.push_sample([START_MARKER]) 
    
    return {"status": "ok"}

@app.post(mainRoute+"/record_timestamp/{record_id}")
def record_timestamp(record_id: str):
    Logger.info(f'Recording timestamp {record_id} at {time.time()}')
    outlet.push_sample([record_id]) 
    return {"status": "ok"}

@app.post(f'{mainRoute}/stop')
def stop():
    Logger.info("Stopping experiment at " + str(time.time()))
    outlet.push_sample([STOP_MARKER])
    return {"status": "ok"}