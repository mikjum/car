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
        
        self.car = car.CarModel(L, d, 45, 100, 2, posX, posY, angle-90, timeD)
        self.surf = pygame.image.load("car.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        #self.surf = pygame.Surface((d, L))
        #self.surf.fill((255, 255, 255))
        
        self.originalsurf = self.surf
        self.rect = self.surf.get_rect(center = (posX,posY))
        
        self.positionX = posX
        self.positionY = posY
        self.angle = angle
        self.cornerpoints = [self.rect.topright, self.rect.topleft, self.rect.bottomleft, self.rect.bottomright]
        cornerangle = math.atan(self.rect.height/self.rect.width)*180/math.pi
      
        cornerdistance = math.sqrt((self.rect.width/2)*(self.rect.width/2) + (self.rect.height/2)*(self.rect.height/2))
        self.cornerangles = [cornerangle, 180-cornerangle, 180+cornerangle, -cornerangle]
        cornerpoints2 = []
        for corner in self.cornerangles:
            cornerpointx = self.rect.centerx + cornerdistance*math.cos(corner*math.pi/180)
            cornerpointy = self.rect.centery - cornerdistance*math.sin(corner*math.pi/180)
            cornerpoints2.append([round(cornerpointx), round(cornerpointy)])
        print (self.cornerpoints)
        print (cornerpoints2)
        print("leveys-pituus", self.rect.width, self.rect.height)
        #self.surf = self.rotate(self.angle)
    
        
    # Rotation of sprite over a pivot point. Point expressed as offset pixels from center point    
    def rotate_point(self, rot, offsetX, offsetY):
        
        
        offsetDistance = math.sqrt(offsetX*offsetX + offsetY*offsetY)
        offsetAngle = math.atan2(offsetY, offsetX)*180/math.pi
    #    print("offsetAngle:", offsetAngle)
        offsetPointOriginalLocationX = offsetDistance*math.sin((self.angle + offsetAngle)*math.pi/180)
        offsetPointOriginalLocationY = offsetDistance*math.cos((self.angle+offsetAngle)*math.pi/180)
     #   print("alkup. erotus", offsetPointOriginalLocationX, offsetPointOriginalLocationY)
        self.angle += rot
        self.rotate(self.angle)
        offsetPointNewLocationX = offsetDistance*math.sin((self.angle+offsetAngle)*math.pi/180)
        offsetPointNewLocationY = offsetDistance*math.cos((self.angle+offsetAngle)*math.pi/180)
        movementX = offsetPointNewLocationX-offsetPointOriginalLocationX
        movementY = offsetPointNewLocationY-offsetPointOriginalLocationY
      #  print("movements", movementX, movementY)
       # print("kulma", self.angle)
        self.rect.move_ip(movementX, movementY)
        
        
    def accelerate(self, acceleration):
        self.car.updateSpeed(acceleration)
        
    def steer(self, steeringAngle):
        self.car.turnWheels(steeringAngle)
    
    def brake(self, brakepower):
        self.car.brake(brakepower)
        
    def update_cornerpoints(self):
        for element in self.cornerpoints:
            pass
        
    
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
        
        
        if self.rect.centerx < 0 or self.rect.centerx > 1500 or self.rect.centery < 0 or self.rect.centery > 900:
            self.car.speed = 0
        
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
        self.rotate_point(deltaA, -40, 0)
        
        
   
        self.rect.move_ip(-muutosX, muutosY)
        
        
    