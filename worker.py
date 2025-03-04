import network_as_code as nac
from network_as_code.models.device import Device, DeviceIpv4Addr
import os

import threading
import time

from zones import zones
from device import device
from utils import Status, OBW, ZoneTypes


API_KEY = os.getenv("API_KEY")

class Worker:
    def __init__(self):
        self._token_expired = False
        self._devices = []
        self._zones = []
        
        self._nac_client = nac.NetworkAsCodeClient(token=API_KEY)
        
        self.initializeZones()
        self.initializeDevices()
        
        self._keep_alive = True
        
        main_thread = threading.Thread(target=self.getDevicesLocationThread)
        main_thread.start()
                
                        
    def stop(self):
        self._keep_alive = False
        while(self._thread_finished):
            time.sleep(0.5)

        print("App has been finished")
        
                
    def initializeDevices(self):
        device1 = device()
        device1.initializeDevice(0,0,"abc123", "worker1", "+34649379033")
        device2 = device()
        device2.initializeDevice(0,0,"def456", "worker2", "+3672123444")
        device3 = device()
        device3.initializeDevice(0,0,"ghi789", "worker3", "+3672123786")
        
        self._devices.append(device1)
        #self._devices.append(device2)
        #self._devices.append(device3)

    def initializeZones(self):
        zone1 = zones()
        zone1.initializeZone(41.371563, 2.152216, 0, 2000, "Work", ZoneTypes.WORK)
        zone2 = zones()
        zone2.initializeZone(41.368520, 2.160378, 1, 2000, "Restricted", ZoneTypes.RESTRICTED)
        zone3 = zones()
        zone3.initializeZone(41.372030, 2.150384, 2, 2000, "SwitchonTalks", ZoneTypes.RESTRICTED)
        
        self._zones.append(zone1)
        self._zones.append(zone2)
        #self._zones.append(zone3)
    
    def getDevicesLocationThread(self):
        
        self._thread_finished = False
        while(self._keep_alive):
            
            for i in range(len(self._zones)):
                zone_info = self._zones[i].getZoneInfo()
                self._zones[i].clearDevices()
                for j in range(len(self._devices)):
                    device_info = self._devices[j].getDeviceInfo()
                    device_nac = self._nac_client.devices.get(phone_number=device_info["phone"])
                    #Get if device in zones
                    try:
                        result = device_nac.verify_location(longitude = zone_info["location"]["long"],
                                                        latitude=zone_info["location"]["lat"],
                                                        radius=zone_info["location"]["rad"],
                                                        max_age=60)
                    except Exception as e:
                        print(f"Error {e}")
                        continue
                    
                    response_type = result.result_type
                    device_status = Status.STATUS_OFFLINE
                    
                    if(zone_info["type"] == ZoneTypes.WORK):
                        if(response_type == "TRUE"):
                            device_status = Status.STATUS_OK
                        else:
                            device_status = Status.STATUS_OFFLINE
                            
                    elif(zone_info["type"] == ZoneTypes.RESTRICTED):
                        if(response_type == "TRUE"):
                            device_status = Status.STATUS_ALARM
                            
                            self._zones[i].addDevice(device_info["id"])
                            
                            if(device_info["obw"] == OBW.ENABLED):
                                print("Skipping OBW already enabled")
                                continue
                                                        
                            self._devices[j].setOptimizedBW(OBW.ENABLED)
                            
                            print(f"Creating QOD for device {device_info["id"]}")
                            #Create QOD service
                            try:
                                session = device_nac.create_qod_session( 
                                            service_ipv4="0.0.0.0",
                                            profile="QOS_E",
                                            duration=OBW.DURATION)   
                                
                            except Exception as e:
                                print(f"Error creating QOD {e}")
                                self._devices[j].setOptimizedBW(OBW.DISABLED)

                                try:
                                    device_nac.clear_sessions()
                                except Exception as ee:
                                    print(f"Error cleaning sessions {e}")       
                        else:
                            continue
                    
                    self._devices[j].setStatus(device_status)
                    
                    #print(f'Zone {zone_info["name"]} = {result.result_type}')
                    
            time.sleep(2)
        print("Exiting main thread")
        self._thread_finished = True

            
    def getDevicesStatus(self):
        #For each device, get the location
        devices_in = []
        
        for i in range(len(self._devices)):
            dev = self._devices[i].getDeviceInfo()
            device_info = {
                "id" : dev["id"],
                "status" : dev["status"],
                "obw" : dev["obw"],
                "location" : dev["location"]
            }
            devices_in.append(device_info)
        
        devices_out = {"devices": devices_in}
            
        return devices_out
    
    def getZones(self):
        zones_info = []
        for i in range(len(self._zones)):
            zones_info.append(self._zones[i].getZoneInfo())
            #ask if a device is in the zone
                        
        response = {"Zones": zones_info}
        return response
    
    def getNumberById(self, id):
        number = ""
        for i in range(len(self._devices)):
            dev_info = self._devices[i].getDeviceInfo()
            if(dev_info["id"] == id):
                number = dev_info["phone"]
                break
        return number
                
        
            
