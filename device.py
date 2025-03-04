from utils import Status, OBW

class device:
    def __init__(self):
        self._lat = 0.0
        self._long = 0.0
        self._id = 0
        self._status = Status.STATUS_OK
        self._name = ""
        self._phone = ""
        self._optimized_bw = OBW.DISABLED
    
    def initializeDevice(self, lat, long, id, name, phone):
        self._lat = lat
        self._long = long
        self._id = id
        self._status = 0
        self._optimized_bw = OBW.DISABLED
        self._name = name
        self._phone = phone
    
    def setStatus(self, status):
        self._status = status
    
    def setOptimizedBW(self, enabled):
        self._optimized_bw = enabled
    
    def getDeviceInfo(self):
        
        info = {"id" : self._id,
                "status" : self._status,
                "name" : self._name,
                "phone" : self._phone,
                "obw" : self._optimized_bw,
                "location": {
                    "lat" : self._lat,
                    "long" : self._long,
                },
                
                }   
        
        return info 