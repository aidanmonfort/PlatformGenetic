import pygame

class Platform:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.getRect())

class Map:
    def __init__(self, grav):
        self.platforms = []
        self.grav = grav

    def getGrav(self):
        return self.grav

    def getPlatforms(self):
        return self.platforms

    def add(self, platform):
        self.platforms.append(platform)

    def draw(self, screen):
        for p in self.platforms:
            p.draw(screen)

class Player:
    def __init__(self):
        self.x = 400
        self.y = 400
        self.dY = 0
        self.dX = 0
        self.width = 30
        self.height = 30
        self.color = (255, 0, 0)
        self.isJump = False

    def setMap(self, map):
        self.map = map

    def step(self):
        self.dY -= self.map.getGrav()
        if(self.dY > 10):
            self.dY = 10
        self.dX *= .95
        self.x += self.dX
        self.y += self.dY
        if self.checkCollision():
            self.isJump = False
            self.x -= self.dX
            self.y -= self.dY

    def jump(self):
        if not self.isJump:
            print("hello")
            self.dY = -20
            self.isJump = True


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def checkCollision(self):
        plats = self.map.getPlatforms()
        for p in plats:
            if p.getRect().colliderect(pygame.Rect(self.x, self.y, self.width, self.height)):
                return True
        return False

