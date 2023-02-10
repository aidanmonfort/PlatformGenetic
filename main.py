import random
import pygame
from Player import *
from DnaStrand import *
from Coins import *


#start the pygame engine
pygame.init()

#start the pygame font engine
pygame.font.init()
myFont = pygame.font.SysFont('Comic Sans MS', 23) #load a font for use

#start the sound engine
pygame.mixer.init()

#game variables
simOver = False
p1 = PlayerAI()
players = []
mapOne = Map(-.5)

#game independent variables (needed for every pygame)
FPS = 60 #60 Frames Per Second for the game update cycle
fpsClock = pygame.time.Clock() #used to lock the game to 60 FPS
screen = pygame.display.set_mode((1280, 720)) #initialize the game window
camera_pos = (0, 0)
world = pygame.Surface((3000,3000))

def createPlayerAI():
    for i in range(50):
        players.append(PlayerAI())


def createMapOne():
    mapOne.add(Platform(0, 690, 2400, 30, (0, 255, 0)))
    mapOne.add(Platform(100, 600, 400, 30, (0, 255, 0)))
    mapOne.add(Platform(200, 500, 400, 30, (0, 255, 0)))
    mapOne.add(Platform(100, 350, 200, 30, (0, 255, 0)))
    mapOne.add(Platform(270, 250, 200, 30, (0, 255, 0)))
    mapOne.add(Platform(600, 200, 30, 400, (0, 255, 0)))
    mapOne.add(Platform(715, 120, 300, 30, (0, 255, 0)))
    mapOne.add(Platform(740, 700, 300, 30, (0, 255, 0)))
    mapOne.add(Coin(600, 650))
    mapOne.add(Coin(220, 450))
    # mapOne.add(Coin())


def draw_mouse_coords():
    textSurface = myFont.render(str(pygame.mouse.get_pos()), True, (255,255,255))
    world.blit(textSurface, (50, 30))
    textSurface = myFont.render(str(players[0].get_current_allele()), True, (255,255,255))
    world.blit(textSurface, (50, 70))
    textSurface = myFont.render(str(len(players)), True, (255, 255, 255))
    world.blit(textSurface, (50, 110))

def clear_screen():
    pygame.draw.rect(world, (0, 0, 0), (0, 0, pygame.Surface.get_height(world), pygame.Surface.get_width(world)))

def input():
    global camera_pos
    if pygame.key.get_pressed()[pygame.K_d]:
        camera_pos = (camera_pos[0] - 10, camera_pos[1])
    if pygame.key.get_pressed()[pygame.K_a]:
        camera_pos = (camera_pos[0] + 10, camera_pos[1])
    if pygame.key.get_pressed()[pygame.K_w]:
        camera_pos = (camera_pos[0], camera_pos[1] + 10)
    if pygame.key.get_pressed()[pygame.K_s]:
        camera_pos = (camera_pos[0], camera_pos[1] - 10)
    if camera_pos[0] < 0:
        camera_pos = (0, camera_pos[1])
    if camera_pos[1] < 0:
        camera_pos = (camera_pos[0], 0)


def sort_ai_by_score():
    for i in range(len(players)-1):
        for j in range(len(players)-2):
            playerOne = players[j]
            playerTwo = players[j+1]
            if playerOne.get_score() < playerTwo.get_score():
                temp = playerOne
                players[j] = playerTwo
                players[j+1] = temp

# no worky
def kill_bottom_half():
    global players
    newList = players[0:int(len(players)/2)]
    players.clear()
    players = newList

createMapOne()
createPlayerAI()
for p in players:
    p.setMap(mapOne)

#main while loop
while not simOver:
    clear_screen()
    #loop through and empty the event queue, key presses
    #buttons, clicks, etc.
    for event in pygame.event.get():
        #if the event is a click on the "X" close button
        if event.type == pygame.QUIT:
           simOver = True

    for p in players:
        p.draw(world)
    mapOne.draw(world)
    input()
    draw_mouse_coords()

    # player update code
    for p in players:
        p.act()

    if players[0].is_done():
        print("done")
        sort_ai_by_score()
        kill_bottom_half()
        for p in players:
            p.reset()



    #put all the graphics on the screen
    #should be the LAST LINE of game code
    screen.blit(world, camera_pos)
    pygame.display.flip()
    fpsClock.tick(FPS) #slow the loop down to 60 loops per second