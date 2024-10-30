# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 13:16:48 2024

@author: MikkoMäkelä-Vaitilo
"""

import pygame
import car_sprite


pygame.init()

clock = pygame.time.Clock()

from pygame.locals import (
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_DOWN,
    K_SPACE,
    QUIT
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900

scalefactor = 37
refreshRate = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

screen.fill([255, 0, 0])



kaara = car_sprite.carSprite(100, 500, 0, 30, 70, refreshRate/1000)



running = True
accelration = 1000
timepassed = 0

while (running):

    
    for event in pygame.event.get():

        # Did the user click the window close button? If so, stop the game.
        if event.type == QUIT:
            pygame.quit()
           # file.close()
           
    pressed_keys = pygame.key.get_pressed()
    
    if pressed_keys[K_UP]:
        kaara.accelerate(10)
    if pressed_keys[K_LEFT]:
        kaara.steer(5)
       # kaara.rotate_point(5, -40, 0)
    if pressed_keys[K_RIGHT]:
        kaara.steer(-5)
    if pressed_keys[K_DOWN]:
        kaara.accelerate(-10)
    if pressed_keys[K_SPACE]:
         kaara.brake(20)
         print(kaara.cornerpoints)
    
       
    # if timepassed > 1000 and timepassed < 3000:
    #     kaara.steer(1)
    # if timepassed > 3000:
    #     kaara.steer(0)
    #print("updeittaa")
    kaara.update()
    pygame.display.update()
    clock.tick(refreshRate)
    timepassed += refreshRate
    screen.fill([255, 0, 0])
    screen.blit(kaara.surf, kaara.rect)
    #print("spriten sijainti")

    


