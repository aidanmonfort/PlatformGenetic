import random
import pygame
from classes import *


#start the pygame engine
pygame.init()

#start the pygame font engine
pygame.font.init()
myFont = pygame.font.SysFont('Comic Sans MS', 23) #load a font for use

#start the sound engine
pygame.mixer.init()

#game variables
simOver = False
p1 = Player()
mapOne = Map(-.5)

#game independent variables (needed for every pygame)
FPS = 60 #60 Frames Per Second for the game update cycle
fpsClock = pygame.time.Clock() #used to lock the game to 60 FPS
screen = pygame.display.set_mode((1280, 720)) #initialize the game window

def createMapOne():
    mapOne.add(Platform(120, 600, 300, 10, (0, 255, 0)))

def clear_screen():
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 720))

def input():
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        p1.jump()

createMapOne()
p1.setMap(mapOne)
#main while loop
while not simOver:
    clear_screen()
    #loop through and empty the event queue, key presses
    #buttons, clicks, etc.
    for event in pygame.event.get():
        #if the event is a click on the "X" close button
        if event.type == pygame.QUIT:
           simOver = True

    input()
    p1.draw(screen)
    p1.step()
    mapOne.draw(screen)
    #put all the graphics on the screen
    #should be the LAST LINE of game code
    pygame.display.flip()
    fpsClock.tick(FPS) #slow the loop down to 60 loops per second