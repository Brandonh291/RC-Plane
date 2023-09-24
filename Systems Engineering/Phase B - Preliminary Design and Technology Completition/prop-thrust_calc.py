# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 16:59:07 2023

@author: brand
"""
import math
import matplotlib.pyplot as plt
import numpy as np
def calculateDrag(AoA, curSpeed):
        if AoA == 0:
            Cd=0.01004
        elif AoA == 5:
            Cd = 0.01213
        elif AoA == 10:
            Cd = 0.02158
        else:
            Cd=0
            print("Incorrect Angle")
        drag=(0.5)*1.225*curSpeed*curSpeed*Cd*1*0.2
        return drag
rpmStep = 1 #seconds
rpmRange = np.arange(0,22000,rpmStep).tolist() # 20 seconds to take off
curSpeed=15.75
propDia=7
propPitch=3
drag=calculateDrag(0,curSpeed)
table=[]
for x in rpmRange:
    thrust = (4.392e-8)*x*(pow(propDia,3.5)/pow(propPitch,0.5))*((4.233e-4)*x*propPitch-curSpeed)-drag
    table.append(thrust)
    
#plt.plot(rpmRange,table)
#plt.xlabel('RPM')
#plt.ylabel('Thrust (N)')
#plt.title('RPM vs Thrust at 15.75 m/s airspeed')

airspeed = np.arange(0,50,0.01).tolist()
thrust_t=[]
propRPM=12.6*2200
for x in airspeed:
    drag=calculateDrag(0,x)
    thrust = (4.392e-8)*propRPM*(pow(propDia,3.5)/pow(propPitch,0.5))*((4.233e-4)*propRPM*propPitch-x)
    thrust_t.append(thrust)
    
plt.plot(airspeed,thrust_t)
plt.xlabel('airspeed (m/s)')
plt.ylabel('Thrust (N)')
plt.title('airspeed vs Thrust')