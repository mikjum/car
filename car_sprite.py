# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 12:22:11 2024
Defines the sprite of a car. Does not contain internal status of car
object itself, but the car dynamic model object does that.

@author: MikkoMäkelä-Vaitilo
"""
import pygame
import dynamic_car_model as car
import math
import numpy as np


from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_LEFT,
    K_RIGHT

)

TOPRIGHT = 0
TOPLEFT = 1
BOTTOMLEFT = 2
BOTTOMRIGHT = 3

X = 0
Y = 1

class carSprite(pygame.sprite.Sprite):
    _scaleFactor = 55
    _Xres = 0
    _Yres = 0
    
    
    
    def rotate(self, angle):
        self.surf = pygame.transform.rotate(self.originalsurf, self.angle)
        self.rect = self.surf.get_rect(center = self.rect.center)
    
    def __init__(self, posX, posY, angle, L, d, timeD):
        super(carSprite, self).__init__()
        
        
        self.surf = pygame.image.load("car.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        
        #self.surf = pygame.Surface((d, L))
        #self.surf.fill((255, 255, 255))
        
        self.originalsurf = self.surf
        self.rect = self.surf.get_rect(center = (posX,posY))
        
        self.car = car.CarModel(self.rect.height, self.rect.width, -20, 30, 30, 45, 100, 2, posX, posY, angle-90, timeD)
        
        self.positionX = posX
        self.positionY = posY
        self.angle = angle
        self.cornerpoints = [np.array([[self.rect.topright[0]], [self.rect.topright[1]]]), 
                             np.array([[self.rect.topleft[0]], [self.rect.topleft[1]]]), 
                             np.array([[self.rect.bottomleft[0]], [self.rect.bottomleft[1]]]), 
                             np.array([[self.rect.bottomright[0]], [self.rect.bottomright[1]]])]
                                      
        # cornerangle = math.atan(self.rect.height/self.rect.width)*180/math.pi
      
        # self.cornerdistance = math.sqrt((self.rect.width/2)*(self.rect.width/2) + (self.rect.height/2)*(self.rect.height/2))
        # self.cornerangles = [cornerangle, 180-cornerangle, 180+cornerangle, -cornerangle]
        # cornerpoints2 = []
        # for corner in self.cornerangles:
        #     cornerpointx = self.rect.centerx + self.cornerdistance*math.cos(corner*math.pi/180)
        #     cornerpointy = self.rect.centery - self.cornerdistance*math.sin(corner*math.pi/180)
        #     cornerpoints2.append([round(cornerpointx), round(cornerpointy)])
        # print (self.cornerpoints)
        # print (cornerpoints2)
        # print("leveys-pituus", self.rect.width, self.rect.height)
        #self.surf = self.rotate(self.angle)
    
        
    # Rotation of sprite over a pivot point. Point expressed as offset pixels from sprite center point    
    def rotate_point(self, rot, offsetX, offsetY):
        
        
        offsetDistance = math.sqrt(offsetX*offsetX + offsetY*offsetY)
        offsetAngle = math.atan2(offsetY, offsetX)*180/math.pi
        offsetPointOriginalLocationX = offsetDistance*math.sin((self.angle + offsetAngle)*math.pi/180)
        offsetPointOriginalLocationY = offsetDistance*math.cos((self.angle+offsetAngle)*math.pi/180)
        self.angle += rot
        self.rotate(self.angle)
        offsetPointNewLocationX = offsetDistance*math.sin((self.angle+offsetAngle)*math.pi/180)
        offsetPointNewLocationY = offsetDistance*math.cos((self.angle+offsetAngle)*math.pi/180)
        movementX = offsetPointNewLocationX-offsetPointOriginalLocationX
        movementY = offsetPointNewLocationY-offsetPointOriginalLocationY
        self.rect.move_ip(movementX, movementY)
        new_cornerpooints = []
      
        for cornerpoint in self.cornerpoints:
            print("täällä")
            translatedPoint = self.rotate_corners(cornerpoint, self.rect.center)
            new_cornerpooints.append(translatedPoint)
            print(translatedPoint)
        self.cornerpoints = new_cornerpooints
        print (self.cornerpoints)
        
        
        
        
        
    def accelerate(self, acceleration):
        self.car.updateSpeed(acceleration)
        
    def steer(self, steeringAngle):
        self.car.turnWheels(steeringAngle)
    
    def brake(self, brakepower):
        self.car.brake(brakepower)
        
    def rotate_corners(self, cornerpoint, rotationpoint):
        x, y = cornerpoint
        cx, cy = rotationpoint
    
        # Convert angle from degrees to radians
        angle_rad = np.radians(self.angle)
    
        # Create the 2D rotation matrix
        rotation_matrix = np.array([
            [np.cos(angle_rad), -np.sin(angle_rad)],
            [np.sin(angle_rad),  np.cos(angle_rad)]
            ])
    
        # Translate point to origin (center as reference)
        translated_point = np.array([x - cx, y - cy])
    
        # Apply the rotation matrix
        rotated_point = np.dot(rotation_matrix, translated_point)
        return rotated_point    
    
    def update(self):
    
     #   self.car.updateSpeed()
     
        deltaX, deltaY , deltaA = self.car.move()
        
        deltaX += self._Xres
        deltaY += self._Yres
        
        muutosX = math.floor(abs(deltaX))
        muutosX = math.copysign(muutosX, deltaX)
        self._Xres = deltaX-muutosX
        
        muutosY = math.floor(abs(deltaY))
        muutosY = math.copysign(muutosY, deltaY)
        self._Yres = deltaY-muutosY
        
        for corner in self.car.corners:
        
            if corner[0] < 0 or corner[0] > 1500 or corner[1] < 0 or corner[1] > 900:
                print (corner)
                self.car.speed = 0
                pygame.draw.circle(self.surf, [0,255,0], self.rect.center, 5)
                
        
        # oldPosX = self.rect.centerx
        # oldPosY = self.rect.centery
        # print("keskipiste", oldPosX, oldPosY)
    
        #newX, newY, self.angle = self.car.getPosition()
        #self.angle += deltaA
        # self.positionX = newX
        # self.positionY = newY
       
        
        # print("oikea keskipiste", newX, newY)
            
            
        # movementX = (self.positionX - oldPosX)
        # movementY = (self.positionY-oldPosY)
        # print("movementX", movementX)
        # print("MovementY", movementY)
        
        
        
        # print("Muutokset", muutosX, muutosY, deltaA)   
        # print("residuaali", self._Xres, self._Yres)
        
        #self.rotate_point(deltaA, -40, 0)
        self.angle += deltaA
        self.rotate(self.angle)
        
        cornerpoint = []
        self.cornerpoints = []
     #   print("Kulmat", self.cornerangles)
     #    for corner in self.cornerangles:
     #        ang = corner + self.angle
     #        cornerpoint.append(self.rect.centerx + self.cornerdistance*math.cos(ang*math.pi/180))
     #        cornerpoint.append(self.rect.centery - self.cornerdistance*math.sin(ang*math.pi/180))
     #        self.cornerpoints.append(cornerpoint)
     #    startPos = (self.cornerpoints[TOPLEFT][X], self.cornerpoints[TOPLEFT][Y])
     #    endPos = (self.cornerpoints[TOPRIGHT][X], self.cornerpoints[TOPRIGHT][Y])
     #    pygame.draw.line(self.surf, [0, 255, 0], startPos, endPos, 3)
     # #   print("Viivan pisteet", startPos, endPos)
        self.rect.move_ip(muutosX, muutosY)
        
        print ("sprite:", self.rect.centerx)
        print("malli:" , self.car.positionX)
        
        
    