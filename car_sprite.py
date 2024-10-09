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
        #self.surf = self.rotate(self.angle)
    
        
        
    
        
    def accelerate(self, acceleration):
        self.car.updateSpeed(acceleration)
        
    def steer(self, steeringAngle):
        self.car.turnWheels(steeringAngle)
    
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
        
        
        
        
        oldPosX = self.rect.centerx
        oldPosY = self.rect.centery
        print("keskipiste", oldPosX, oldPosY)
    
        #newX, newY, self.angle = self.car.getPosition()
        self.angle += deltaA
        # self.positionX = newX
        # self.positionY = newY
       
        
        # print("oikea keskipiste", newX, newY)
            
            
        # movementX = (self.positionX - oldPosX)
        # movementY = (self.positionY-oldPosY)
        # print("movementX", movementX)
        # print("MovementY", movementY)
        
        
        
        print("Muutokset", muutosX, muutosY, deltaA)   
        print("residuaali", self._Xres, self._Yres)
        self.rotate(self.angle)
        
        
   
        self.rect.move_ip(-muutosX, muutosY)
        
        
    