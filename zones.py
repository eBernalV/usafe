from utils import Status, ZoneTypes

class zones:
    def __init__(self):
        self._lat = 0.0
        self._long = 0.0
        self._id = 0
        self._rad = 2000
        self._status = Status.STATUS_OK
        self._name = ""
        self._type = ZoneTypes.WORK
        self._devices_in = []
    
    def initializeZone(self, lat, long, id, rad, name, type):
        self._lat = lat
        self._long = long
        self._id = id
        self._rad = rad
        self._status = 0
        self._name = name
        self._type = type
        self._devices_in = []
    
    def setStatus(self, status):
        self._status = status
    
    def addDevice(self, id):
        dev = {"id" : id }
        self._devices_in.append(dev)
        
    def clearDevices(self):
        self._devices_in = []
    
    def getZoneInfo(self):
        
        info = {"id" : self._id,
                "status" : self._status,
                "name" : self._name,
                "type" : self._type,
                "location": {
                    "lat" : self._lat,
                    "long" : self._long,
                    "rad" : self._rad
                },
                "devices" : self._devices_in
                }   
        
        return info 