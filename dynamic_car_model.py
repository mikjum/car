# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 09:47:17 2024

Dynamic model for a car. Defines the state of car object and calculates 
movements on 2d space based on speed, angurar position and angle of front tires.

contains methods:
    updateSpeed(acceleration)   Adds argument acceleration value to internal speed value
                                There is limiting factor top speed that cannot be exceeded  
    turnWheels(angularMovement) changes the angle of tires based on argument
                                Limiting factor is the maximum turn angle
                                
    move()                      Calculates the change on X- and Y- axis and the car
                                angular position based on intenal values. Timedelta
                                value (set in initialization) defines how often car 
                                position is updated, so the calculations are correct
                                on time. ToDo: consider not using constant timedelta,
                                but storing the time exceeded since last call and 
                                calculating values according to that.
                                
    getPosition()               Returs the current position (x- and Y coordinates and
                                                             angular position)

@author: MikkoMäkelä-Vaitilo
"""

import math
import numpy as np


class CarModel():
    
    def __init__(self, length, width, axleoffset, wheelBase, gauge, maxWheelAngle, maxSpeed, maxAcceleration, positionX, positionY, initRotation, timeDelta):
        self.wheelBase = wheelBase
        self.gauge = gauge
        self.maxWheelAngle = maxWheelAngle
        self.maxSpeed = maxSpeed
        self.maxAcceleration = maxAcceleration
        self.positionX = positionX
        self.positionY = positionY
        self.rotation = initRotation
        self.axleOffset = -20
        self.speed = 0.0
        self.acceleration = 0.0
        self.wheelAngle = 0.0
        self.timeDelta = timeDelta
        
        
        self.length = length
        self.width = width
        


    # def accelerate(self, acceleration):
    #     self.acceleration = acceleration
        
    # def setSteering(self, angle):
    #     self.wheelAngle = angle
        
    def updateSpeed(self, acceleration):
        newSpeed = self.speed + acceleration * self.timeDelta

        if newSpeed > self.maxSpeed:
    
            self.speed = self.maxSpeed
        else:
            self.speed = newSpeed
            
    def calculateCorners(self):
        corners = []
        cornerDeltaX = self.width/2
        cornerDeltaY = self.length/2
        
        cornerTransfer = [[-cornerDeltaX, -cornerDeltaY], 
                          [cornerDeltaX, -cornerDeltaY],
                          [cornerDeltaX, cornerDeltaY],
                          [-cornerDeltaX, cornerDeltaY]]
        
        for cornerT in cornerTransfer:
            cornerX = self.positionX + cornerT[0]*math.cos(self.rotation*math.pi/180) + cornerT[1]*math.sin(self.rotation*math.pi/180)
            cornerY = self.positionY - cornerT[0]*math.sin(self.rotation*math.pi/180) + cornerT[1]*math.cos(self.rotation*math.pi/180)
            corners.append([cornerX, cornerY])
            
        self.corners = corners
        print (corners)
            
        
        
    def brake(self, bpower):
        newSpeed = self.speed - bpower
        if newSpeed < 0:
            newSpeed = 0
        self.speed = newSpeed
        
    def turnWheels(self, turningAngle):
        newAngle = self.wheelAngle + turningAngle
        if abs(newAngle) > self.maxWheelAngle:
            self.wheelAngle = math.copysign(self.maxWheelAngle, newAngle)
        else:
            self.wheelAngle = newAngle
    
    #poerforms rotation around back axis midpoint so that actual car midpoint 
    # moves accordingly as a side effect.
    def rotate_midpoint(self, omega):
        offsetDistance = self.axleOffset
        offsetAngle = -90
        offsetPointOriginalLocationX = offsetDistance*math.sin((self.rotation + offsetAngle)*math.pi/180)
        offsetPointOriginalLocationY = offsetDistance*math.cos((self.rotation+offsetAngle)*math.pi/180)
        self.rotation += omega
        offsetPointNewLocationX = offsetDistance*math.sin((self.rotation+offsetAngle)*math.pi/180)
        offsetPointNewLocationY = offsetDistance*math.cos((self.rotation+offsetAngle)*math.pi/180)
        movementX = offsetPointNewLocationX-offsetPointOriginalLocationX
        movementY = offsetPointNewLocationY-offsetPointOriginalLocationY
        print ("offsetit: ", movementX, movementY)
        return movementX, movementY
        # self.positionX += movementX
        # self.positionY += movementY
        
  
        
    def move(self):
     
   #     print("Steering angle:", self.wheelAngle)
        omega = (self.speed/self.wheelBase)*math.tan(self.wheelAngle*math.pi/180)
        movX, movY = self.rotate_midpoint(omega)
        #self.rotation += omega
        xDelta = movX -  math.cos(self.rotation*math.pi/180)*self.speed*self.timeDelta
        self.positionX += xDelta
        yDelta = movY +  math.sin(self.rotation*math.pi/180)*self.speed*self.timeDelta
        self.positionY += yDelta
        self.calculateCorners()
        
        return xDelta, yDelta, omega
    
    def getPosition(self):
        return self.positionX, self.positionY, self.rotation
    
    
        
        
        
        

        