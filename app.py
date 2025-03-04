from flask import Flask, request, jsonify
import json
import signal
import sys

from worker import Worker
from utils import Status, OBW


app = Flask(__name__)
myworker = Worker()


def signalHandler():
    myworker.stop() 
    sys.exit(0)

#getZonesStatus
@app.route('/getZonesStatus')
def getZonesStatus():
    zones = myworker.getZones()    
    
    return json.dumps(zones, indent = 4)


#getOperatorStatus
@app.route("/getOperatorStatus")
def getOperatorStatus():
    operators = []

    return json.dumps(operators, indent = 4)

#getNumber
@app.route("/getNumber/<string:id>")
def getNumber(id):
    number = myworker.getNumberById(id)
    response = {"id" : id,
                "number": number}
    
    return json.dumps(response, indent = 4)

#getDevicesStatus
@app.route("/getDevicesStatus")
def getDevicesStatus():
    devices = myworker.getDevicesStatus()
    return json.dumps(devices, indent = 4)

#Stops the main thread
signal.signal(signal.SIGINT, signalHandler)

app.run()
