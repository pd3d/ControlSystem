"""
Stethoscope Demo :: Tracking

The following code was built to show the heart-rate tracking capabilities of the stethoscope

Fluvio L Lobo Fenoglietto
01/31/2017
"""

# Import
import  sys
import  os
import  serial
import  time
import  stethoscopeDefinitions       as     definitions
from    os.path                      import expanduser
from    bluetoothProtocol_teensy32   import *
from    stethoscopeProtocol          import *

# Operation


print fullStamp() + " Connecting to the Stethoscope"
deviceName = "SS"
portNumber = 0
deviceBTAddress = "00:06:66:7D:99:D9"
baudrate = 115200
attempts = 5
rfObject = createPort(deviceName,portNumber,deviceBTAddress,baudrate,attempts)

print fullStamp() + " Enquiring Stethoscope Status"
time.sleep(1)
statusEnquiry(rfObject,attempts)

print fullStamp() + " Triggering Heart Rate Tracking"
time.sleep(1)
startTrackingMicStream(rfObject,attempts)

print fullStamp() + " Openning Stethoscope Serial Port"
time.sleep(1)
if rfObject.isOpen() == False:
    rfObject.open()

tracking_start_time = time.time()
tracking_stop_time = 30
tracking_current_time = 0
dataStream = []
print fullStamp() + " Tracking Heart Rate for %.03f seconds" %tracking_stop_time
while tracking_current_time < tracking_stop_time:
    
    dataStream.append(["%.02f" %tracking_current_time,
                       rfObject.readline()[:-1]])
    
    tracking_current_time = time.time() - tracking_start_time
    print fullStamp() + " Current Simulation Time = %.03f" %tracking_current_time

print fullStamp() + " Closing Stethoscope Serial Port"
time.sleep(1)
rfObject.close()

print fullStamp() + " Stopping Device Streaming"
time.sleep(1)
stopTrackingMicStream(rfObject,attempts)

print fullStamp() + " Releasing Serial Port"
time.sleep(1)
portRelease('rfcomm', 0)

