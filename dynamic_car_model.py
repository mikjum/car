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



class CarModel():
    
    def __init__(self, wheelBase, gauge, maxWheelAngle, maxSpeed, maxAcceleration, positionX, positionY, initRotation, timeDelta):
        self.wheelBase = wheelBase
        self.gauge = gauge
        self.maxWheelAngle = maxWheelAngle
        self.maxSpeed = maxSpeed
        self.maxAcceleration = maxAcceleration
        self.positionX = positionX
        self.positionY = positionY
        self.rotation = initRotation
        self.speed = 0.0
        self.acceleration = 0.0
        self.wheelAngle = 0.0
        self.timeDelta = timeDelta

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
    
  
        
    def move(self):
     
   #     print("Steering angle:", self.wheelAngle)
        omega = (self.speed/self.wheelBase)*math.tan(self.wheelAngle*math.pi/180)
        self.rotation += omega
        xDelta = math.cos(self.rotation*math.pi/180)*self.speed*self.timeDelta
        self.positionX += xDelta
        yDelta = math.sin(self.rotation*math.pi/180)*self.speed*self.timeDelta
        self.positionY += yDelta
        
        return xDelta, yDelta, omega
    
    def getPosition(self):
        return self.positionX, self.positionY, self.rotation
    
        
        
        
        

        