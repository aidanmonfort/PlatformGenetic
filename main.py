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
numPlayers = 50
gen = 0
onlyLeader = False

def createPlayerAI():
    for i in range(numPlayers):
        players.append(PlayerAI())


def createMapOne():
    mapOne.add(Platform(0, 690, 2400, 30))
    mapOne.add(Platform(2400, 0, 30, 730))
    mapOne.add(Platform(100, 600, 400, 30))
    mapOne.add(Platform(200, 500, 400, 30))
    mapOne.add(Platform(100, 350, 200, 30))
    mapOne.add(Platform(270, 250, 200, 30))
    mapOne.add(Platform(600, 200, 30, 400))
    mapOne.add(Platform(715, 120, 300, 30))
    mapOne.add(Platform(740, 700, 300, 30))
    mapOne.add(Platform(750, 550, 300, 30))
    mapOne.add(Platform(-10, 0, 20, 720))
    mapOne.add(Platform(800, 450, 300, 30))
    mapOne.add(Platform(1300, 475, 300, 30))
    mapOne.add(Platform(1170, 300, 600, 30))
    mapOne.add(Coin(600, 650))
    mapOne.add(Coin(220, 430))
    mapOne.add(Coin(730, 80))
    mapOne.add(Coin(780, 80))
    mapOne.add(Coin(830, 80))
    mapOne.add(Coin(880, 80))
    mapOne.add(Coin(775, 510))
    mapOne.add(Coin(850, 510))
    mapOne.add(Coin(850, 410))
    mapOne.add(Coin(1230, 260))
    mapOne.add(Coin(1300, 260))
    mapOne.add(Coin(1450, 410))


def draw_mouse_coords():
    global camera_pos
    textSurface = myFont.render(str(pygame.mouse.get_pos()), True, (255,255,255))
    world.blit(textSurface, (50 - camera_pos[0], 30 - camera_pos[1]))
    textSurface = myFont.render(str(players[0].get_current_allele()), True, (255,255,255))
    world.blit(textSurface, (50 - camera_pos[0], 70 - camera_pos[1]))
    textSurface = myFont.render(str(len(players)), True, (255, 255, 255))
    world.blit(textSurface, (50 - camera_pos[0], 110 - camera_pos[1]))
    textSurface = myFont.render(f'Gen: {gen}', True, (255, 255, 255))
    world.blit(textSurface, (50 - camera_pos[0], 150 - camera_pos[1]))




def clear_screen():
    pygame.draw.rect(world, (0, 0, 0), (0, 0, pygame.Surface.get_height(world), pygame.Surface.get_width(world)))

def buttons():
    global camera_pos, onlyLeader

    if pygame.key.get_pressed()[pygame.K_d]:
        camera_pos = (camera_pos[0] - 10, camera_pos[1])
    if pygame.key.get_pressed()[pygame.K_a]:
        camera_pos = (camera_pos[0] + 10, camera_pos[1])
    if camera_pos[0] > 0:
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

def kill_bottom_half():
    global players
    newList = players[0:int(len(players)/2)]
    players.clear()
    players = newList

def mutate(dna):
    newDna = [num for num in dna if random.randint(1, 100) < 95]
    while len(newDna) < PlayerAI.count:
        choice = rand.randint(1, 100)
        if choice <= 80:
            newDna.append(0)
        elif choice <= 86:
            newDna.append(1)
        elif choice <= 93:
            newDna.append(2)
        elif choice <= 100:
            newDna.append(3)
    return newDna


def createKids():
    global players
    mom = players[random.randint(0, len(players) - 1)]
    dad = players[random.randint(0, len(players) - 1)]
    index = random.randint(0, mom.count)
    momDNA = mom.strand[0:index]
    dadDNA = dad.strand[index:]
    dna = momDNA + dadDNA
    child = PlayerAI()
    child.setDNA(mutate(dna))
    child.setMap(mom.player.map)
    players.append(child)

def reset():
    global gen
    sort_ai_by_score()
    kill_bottom_half()
    while len(players) < numPlayers:
        createKids()
    for p in players:
        p.reset()
    for coin in mapOne.coins:
        coin.changeColor((255, 255, 0))
    gen += 1

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
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            onlyLeader = not onlyLeader

    if not onlyLeader:
        for p in players:
            p.draw(world)
        mapOne.draw(world)
        pygame.draw.circle(world, (255, 0, 0), (players[0].player.x + 15, players[0].player.y + 15), 40, 2)
    else:
        players[0].draw(world)
        for coin in mapOne.coins:
            coin.changeColor((255, 255, 0))
        for plat in mapOne.platforms:
            plat.draw(world)
        for coin in mapOne.coins:
            #weird := is called a walrus operator, basically declares a variable inside an if statement
            if not players[0].player.captured_coins[n := mapOne.coins.index(coin)]:
                coin.draw(world, n)
    buttons()
    draw_mouse_coords()

    # player update code
    for p in players:
        p.act()

    if players[0].is_done():
        reset()



    #put all the graphics on the screen
    #should be the LAST LINE of game code
    screen.blit(world, camera_pos)
    pygame.display.flip()
    fpsClock.tick(FPS) #slow the loop down to 60 loops per second