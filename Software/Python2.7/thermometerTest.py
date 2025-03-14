
# Import
import sys
import os
from os.path import expanduser
import serial
from configurationProtocol import *
from bluetoothProtocol import *
from thermometerProtocol import *

# Variables
# ----------------------------------------------
# B) Path/Directory Variables
# ----------------------------------------------
homeDir = expanduser("~")
rootDir = "/root"
if homeDir == rootDir:
          homeDir = "/home/pi"
          # This check and correction is needed for raspbian
# .../Python
consysPyDir = homeDir + "/csec/repos/ControlSystem/Software/Python"
# .../Python/data
consysPyDataDir = consysPyDir + "/data"
# .../Python/data/scenarios
scenarioConfigFilePath = consysPyDataDir + "/scenarios"

# Scenario File Name
scenarioFileName = "sc001.xml"

configFile = scenarioConfigFilePath + "/" + scenarioFileName
tree, root = readConfigFile(configFile)

# =========
# OPERATION
# =========

#deviceName, deviceBTAddress = pullInstruments(tree, root)   # pull instrument information from configuration file
deviceName = "hola"
deviceBTAddress = "00:06:66:86:76:C5"
rfObject = createPort(deviceName, deviceBTAddress, 115200, 20)          # create rfObjects/ports

#statusEnquiry(rfObject, 5, 5)
startSIMold(rfObject, 5, 5)
#deviceID(rfObject)


portRelease('rfcomm', 0)                                    # Release port to avoid permanent connection
