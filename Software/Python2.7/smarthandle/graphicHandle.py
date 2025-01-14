"""
graphicHandle.py

The following code has been designed to visualize the motion of the Smart Handle using the data from the 9 DOFs IMU and a few python visualization libraries and/or modules

Fluvio L. Lobo Fenoglietto 06/28/2016
"""

# ===================================
# Import Libraries and/or Modules
# ===================================

# import pywin
# pywin - Python for Windows - Only needed if working on windows
import serial
# if not present:
# > sudo apt-get install python-serial
from visual import *
# if not present:
# > sudo apt-get install python-visual
# Note that this visualization package seems to be outdated
# Implementations of mathematical (numpy, scipy) and plotting packages (Matplotlib) should replace this module in the near future
import string
import math
from time import time

# ===================================
# Operation
# ===================================

# ===================================
# Setting-up Scene
# ===================================

# Scene 1: Representation of the handle
#   Scene Properties
scene = display(title="9DOF IMU Test",x=0,y=0)
scene.width = 1000
scene.height = 1000
scene.range=(1.5,1.5,1.5)
scene.forward = (1,0,-0.25)
scene.up=(0,0,1)
#   Scene Objects
scene.select()
# Reference axis (x,y,z)
arrow(color=color.green,axis=(1,0,0), shaftwidth=0.02, fixedwidth=1)
arrow(color=color.green,axis=(0,-1,0), shaftwidth=0.02 , fixedwidth=1)
arrow(color=color.green,axis=(0,0,-1), shaftwidth=0.02, fixedwidth=1)
# labels
label(pos=(0,0,0.8),text="9DOF IMU Test",box=0,opacity=0)
label(pos=(1,0,0),text="X",box=0,opacity=0)
label(pos=(0,-1,0),text="Y",box=0,opacity=0)
label(pos=(0,0,-1),text="Z",box=0,opacity=0)
# IMU object
platform = box(length=1, height=0.05, width=1, color=color.red)
p_line = box(length=1,height=0.08,width=0.1,color=color.yellow)
plat_arrow = arrow(color=color.green,axis=(0,1,0), shaftwidth=0.06, fixedwidth=1)

# Scene 2: Second scene (Roll, Pitch, Yaw)
#scene2 = display(title='9DOF Razor IMU test',x=0, y=0, width=500, height=200,center=(0,0,0), background=(0,0,0))
#scene2.range=(1,1,1)
#scene2.select()
#Roll, Pitch, Yaw
#cil_roll = cylinder(pos=(-0.4,0,0),axis=(0.2,0,0),radius=0.01,color=color.red)
#cil_roll2 = cylinder(pos=(-0.4,0,0),axis=(-0.2,0,0),radius=0.01,color=color.red)
#cil_pitch = cylinder(pos=(0.1,0,0),axis=(0.2,0,0),radius=0.01,color=color.green)
#cil_pitch2 = cylinder(pos=(0.1,0,0),axis=(-0.2,0,0),radius=0.01,color=color.green)
#arrow_course = arrow(pos=(0.6,0,0),color=color.cyan,axis=(-0.2,0,0), shaftwidth=0.02, fixedwidth=1)

#Roll,Pitch,Yaw labels
#label(pos=(-0.4,0.3,0),text="Roll",box=0,opacity=0)
#label(pos=(0.1,0.3,0),text="Pitch",box=0,opacity=0)
#label(pos=(0.55,0.3,0),text="Yaw",box=0,opacity=0)
#label(pos=(0.6,0.22,0),text="N",box=0,opacity=0,color=color.yellow)
#label(pos=(0.6,-0.22,0),text="S",box=0,opacity=0,color=color.yellow)
#label(pos=(0.38,0,0),text="W",box=0,opacity=0,color=color.yellow)
#label(pos=(0.82,0,0),text="E",box=0,opacity=0,color=color.yellow)
#label(pos=(0.75,0.15,0),height=7,text="NE",box=0,color=color.yellow)
#label(pos=(0.45,0.15,0),height=7,text="NW",box=0,color=color.yellow)
#label(pos=(0.75,-0.15,0),height=7,text="SE",box=0,color=color.yellow)
#label(pos=(0.45,-0.15,0),height=7,text="SW",box=0,color=color.yellow)

#L1 = label(pos=(-0.4,0.22,0),text="-",box=0,opacity=0)
#L2 = label(pos=(0.1,0.22,0),text="-",box=0,opacity=0)
#L3 = label(pos=(0.7,0.3,0),text="-",box=0,opacity=0)

# Scene 3: Proximity
#   Scene Properties
scene3 = display(title="Proximity of Handle",x=1000,y=0)
scene3.width = 1000
scene3.height = 1000
scene3.range=(1.2,1.2,1.2)
#   Scene Objects
ball = sphere(pos = vector(-0.5,0,0), radius=0.10, color=color.green)
wall = box(pos = vector(0,0,0), length=0.05, height=0.5, width=1, color=color.red)
#wall = sphere(pos = vector(0.5,0,0), radius=0.10, color=color.cyan)
#   Scene Labels
gap = label(pos=(0,-0.5,0),text="Distance = 00.00 mm",box=0,opacity=0)
#gapValue = label(pos=(0.11,-0.5,0),text="00.00 mm",box=0,opacity=0)


# ===================================
# Serial Connection
# ===================================

grad2rad = 3.141592/180.0
ser = serial.Serial(port='/dev/ttyUSB0',baudrate=115200, timeout=1)

roll=0
pitch=0
yaw=0
gapVal = 0.5

# Proximity Parameters
maxGap = 120

while True:
    
    line = ser.readline()
    words = string.split(line,",")    # Fields split
    # print words
    if len(words) > 2:
        try:
            pitch = float(words[13])*grad2rad
            # print pitch
            roll = float(words[15])*grad2rad
            # print roll
            yaw = float(words[17])*grad2rad
            # print yaw

            #L1.text = str(float(words[15]))
            #L2.text = str(float(words[13]))
            #L3.text = str(float(words[17]))
            gap.text = "Distance = " + str(float(words[21])) + " mm"
            gapReadout = float(words[21])
            print gapReadout
            gapRatio = gapReadout/maxGap
            gapVal = gapRatio
        
        except:
            print "Invalid line"

        axis=(cos(pitch)*cos(yaw),-cos(pitch)*sin(yaw),sin(pitch)) 
        up=(sin(roll)*sin(yaw)+cos(roll)*sin(pitch)*cos(yaw),sin(roll)*cos(yaw)-cos(roll)*sin(pitch)*sin(yaw),-cos(roll)*cos(pitch))
        platform.axis=axis
        platform.up=up
        platform.length=1.0
        platform.width=0.65
        plat_arrow.axis=axis
        plat_arrow.up=up
        plat_arrow.length=0.8
        p_line.axis=axis
        p_line.up=up
        #cil_roll.axis=(0.2*cos(roll),0.2*sin(roll),0)
        #cil_roll2.axis=(-0.2*cos(roll),-0.2*sin(roll),0)
        #cil_pitch.axis=(0.2*cos(pitch),0.2*sin(pitch),0)
        #cil_pitch2.axis=(-0.2*cos(pitch),-0.2*sin(pitch),0)
        #arrow_course.axis=(0.2*sin(yaw),0.2*cos(yaw),0)

        # Update Scene 3:
        ball.pos = vector(-gapVal,0,0)
        
        
ser.close
f.close


"""
References
1- Installing Python Serial - https://www.raspberrypi.org/forums/viewtopic.php?f=5&t=5938
2- IMU Guide - http://webbot.org.uk/iPoint/49.page

"""
