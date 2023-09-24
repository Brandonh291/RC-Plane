# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 11:01:22 2023

@author: brand
"""
import math
import matplotlib.pyplot as plt
import numpy as np
timeStep = 0.01 #seconds
timeRange = np.arange(0,5,timeStep).tolist() # 20 seconds to take off
# reynolds is 200k
class Aircraft():
    def __init__(self, weight, wingAvgChord, wingSpan):
        self.wingArea = wingAvgChord * wingSpan # square meters
        self.xVel=0
        self.yVel=0
        self.xPos=0
        self.yPos=0
        self.weight=weight

    def calculateLift(self, AoA, curSpeed):
        if AoA == 0:
            Cl=0.4304
        elif AoA == 5:
            Cl = 0.9118
        elif AoA== 10:
            Cl = 1.2591
        else:
            Cl=0
            print("Incorrect Angle")
        self.lift=(0.5)*1.225*curSpeed*curSpeed*Cl*self.wingArea # Newtons
        
    def calculateDrag(self, AoA, curSpeed):
        if AoA == 0:
            Cd=0.01004
        elif AoA == 5:
            Cd = 0.01213
        elif AoA == 10:
            Cd = 0.02158
        else:
            Cd=0
            print("Incorrect Angle")
        self.drag=(0.5)*1.225*curSpeed*curSpeed*Cd*self.wingArea # Newtons
    
    def calculatePropThrust(self, curSpeed, propDia, propPitch, propRPM):
        self.thrust = (4.392e-8)*propRPM*(pow(propDia,3.5)/pow(propPitch,0.5))*((4.233e-4)*propRPM*propPitch-curSpeed)
        #print(self.thrust)
        
    def calculateForces(self,AoA):
        if self.yPos==0:
            fric_force=self.weight*9.81*0.1
        else:
            fric_force=0
        self.xForces = math.cos(math.radians(AoA))*(self.thrust-self.drag)-fric_force
        self.yForces = math.cos(math.radians(AoA))*(self.lift)-self.weight*9.81
        #print(self.yForces)
        
    def calcVel(self,timeStep):
        self.xVel=self.xForces*timeStep+self.xVel
        self.yVel=self.yForces*timeStep+self.yVel

    
    def calcPos(self,timeStep):
        self.xPos = self.xVel*timeStep + self.xPos
        self.yPos = self.yVel*timeStep + self.yPos
        if self.yPos<0:
            self.yPos=0
            self.yVel=0


class PID():
    def __init__(self,P,I,D,step):
        self.pGain=P
        self.iGain=I
        self.dGain=D
        self.step=step
        self.p=0
        self.i=0
        self.d=0
        self.errSum=0
        self.errPrev=0
    
    def gain(self,curAlt,tarAlt):
        err=tarAlt-curAlt
        self.i=self.errSum+err*self.step
        self.d = (err-self.errPrev)/self.step
        self.output=err*self.pGain + self.iGain*self.i + self.dGain*self.d
        self.errPrev=err
        self.errSum=self.i
        self.output = max(min(22000,self.output),0)
        #print(self.output)
               
        
# 0 AoA
plane = Aircraft(1.3, 0.2, 1)
control = PID(700,140/2,140/8,timeStep)
xPos=[]
yPos=[]
xVel=[]
yVel=[]
lift=[]
thrust=[]
curSpeed=0
AoA=0
RPM_l=[]
RPM=22000

for x in timeRange:
    plane.calculateLift(AoA,curSpeed)
    plane.calculateDrag(AoA,curSpeed)
    plane.calculatePropThrust(curSpeed,7,3,RPM)
    plane.calculateForces(AoA)
    plane.calcVel(timeStep)
    plane.calcPos(timeStep)
    xPos.append(plane.xPos)
    yPos.append(plane.yPos)
    curSpeed=plane.xVel
    xVel.append(plane.xVel)
    yVel.append(plane.yVel)
    lift.append(plane.yForces)
    thrust.append(plane.thrust)
    #RPM_l.append(control.output/1000)    


#plt.plot(timeRange,yPos/199)
#plt.plot(timeRange,thrust)

#plt.plot(timeRange,lift)
#plt.plot(timeRange,xPos)
plt.plot(timeRange,yPos)
#plt.plot(timeRange,thrust)
#plt.plot(timeRange, RPM_l)
#plt.plot(timeRange,yVel)
plt.legend(['alt'])
plt.xlabel('Time (s)')
plt.ylabel(['Meters'])