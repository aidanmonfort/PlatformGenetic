import pygame
from Map import *

class Player:
    def __init__(self, color=(255, 255, 255)):
        self.x = 400
        self.y = 400
        self.dY = 0
        self.dX = 0
        self.width = 30
        self.height = 30
        self.color = color
        self.isJump = False
        self.score = 0

    def setMap(self, map):
        self.map = map
        self.captured_coins = [False for i in range(len(map.coins))]

    def step(self):
        self.dY -= self.map.getGrav()
        if self.dY > 10:
            self.dY = 10
        self.dX *= .75
        self.x += self.dX
        self.y += self.dY
        if self.is_map_bottom_collision():
            self.y -= self.dY
            self.isJump = False
        if self.is_map_right_collision():
            self.x -= self.dX

        self.checkCoinCollisions()

        return self.x, self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def jump(self):
        if not self.isJump:
            self.dY = -15
            self.isJump = True

    def checkCoinCollisions(self):
        for c in self.map.coins:
            if c.getCollisionRect().colliderect(self.getCollisionRect()):
                self.score += 1
                self.captured_coins[self.map.coins.index(c)] = True
                c.changeColor(self.color)

    def stepRight(self):
        self.dX = 10

    def stepLeft(self):
        self.dX = -10

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.getCollisionRect())

    def getCollisionRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_map_collision(self):
        myHitBox = pygame.Rect(self.x, self.y, self.width, self.height)
        mapHitBoxes = self.map.get_hit_box_list()
        for box in mapHitBoxes:
            if myHitBox.colliderect(box):
                return True

        return False

    def is_map_bottom_collision(self):
        myHitBox = pygame.Rect(self.x, self.y, self.width, self.height)
        myBottomY = myHitBox.y + myHitBox.height
        mapHitBoxes = self.map.get_hit_box_list()
        for box in mapHitBoxes:
            if myHitBox.colliderect(box):
                if myBottomY > box.y: # I am hitting and BELOW this platform
                    return True

        return False


    def is_map_right_collision(self):
        myHitBox = pygame.Rect(self.x, self.y, self.width, self.height)
        myRightX = myHitBox.x + myHitBox.width
        mapHitBoxes = self.map.get_hit_box_list()
        for box in mapHitBoxes:
            if myHitBox.colliderect(box):
                if myRightX > box.x: # I am hitting and to the RIGHT this platform
                    return True

        return False

    def get_score(self):
        return len([c for c in self.captured_coins if c])


