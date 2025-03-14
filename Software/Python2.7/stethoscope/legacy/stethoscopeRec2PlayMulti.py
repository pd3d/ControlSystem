"""
Stethoscope Demo :: Blending

The following code was built to show the recording capabilities of the stethoscope

Fluvio L Lobo Fenoglietto
04/22/2017
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


print fullStamp() + " Connecting to the Stethoscopes"
deviceName = "SS"
deviceBTAddress = ["00:06:66:86:77:09","00:06:66:86:60:02","00:06:66:8C:D3:F6"]
baudrate = 115200
attempts = 5

rfObject = []
for i in range(0,len(deviceBTAddress)):
    rfObject.append(createPort(deviceName,i,deviceBTAddress[i],baudrate,attempts))

print fullStamp() + " Enquiring Stethoscope Status"

for i in range(0,len(deviceBTAddress)):
    time.sleep(1)
    statusEnquiry(rfObject[i],attempts)


print fullStamp() + " Start Recording"
for i in range(0,len(deviceBTAddress)):
    time.sleep(1)
    startRecording(rfObject[i],attempts)

print fullStamp() + " Opening Stethoscopes Serial Port"
for i in range(0,len(deviceBTAddress)):
    time.sleep(1)
    if rfObject[i].isOpen() == False:
        print fullStamp() + " Opening Serial Port " + str(i)
        rfObject[i].open()

tracking_start_time = time.time()
tracking_stop_time = 20
tracking_current_time = 0
dataStream = []
dataStream
print fullStamp() + " Recording and Tracking Heart Rate for %.03f seconds" %tracking_stop_time
while tracking_current_time < tracking_stop_time:

    dataStream.append(["%.02f" %tracking_current_time,
                       rfObject[0].readline()[:-1],
                       rfObject[1].readline()[:-1],
                       rfObject[2].readline()[:-1]])
    
    tracking_current_time = time.time() - tracking_start_time
    print fullStamp() + " Current Simulation Time = %.03f" %tracking_current_time

print fullStamp() + " Closing Stethoscopes Serial Port"
for i in range(0,len(deviceBTAddress)):
    time.sleep(1)
    if rfObject[i].isOpen() == True:
        print fullStamp() + " Closing Serial Port " + str(i)
        rfObject[i].close()

print fullStamp() + " Stop Recording"
for i in range(0,len(deviceBTAddress)):
    time.sleep(1)
    stopRecording(rfObject[i],attempts)

print fullStamp() + " Start Blending Recorded File"
fileByte = definitions.BRECORD
for i in range(0,len(deviceBTAddress)):
    time.sleep(1)
    startBlending(rfObject[i],fileByte,attempts)

tracking_stop_time = 20
print fullStamp() + " Blend for %.03f seconds" %tracking_stop_time
time.sleep(20)

print fullStamp() + " Stop Blending Recorded File"
for i in range(0,len(deviceBTAddress)):
    time.sleep(1)
    stopBlending(rfObject[i],attempts)

for i in range(0,len(deviceBTAddress)):
    time.sleep(1)
    portRelease('rfcomm', i)

