import pygame
from Platform import *

class Map:
    def __init__(self, grav=-.5):
        self.platforms = []
        self.coins = []
        self.grav = grav

    def getGrav(self):
        return self.grav

    def getPlatforms(self):
        return self.platforms

    def add(self, platformOrCoin):
        if isinstance(platformOrCoin, Platform):
            self.platforms.append(platformOrCoin)
        else:
            self.coins.append(platformOrCoin)

    def draw(self, screen):
        for p in self.platforms:
            p.draw(screen)
        for c in self.coins:
            c.draw(screen)

    def get_hit_box_list(self):
        hitBoxes = []
        for p in self.platforms:
            hitBoxes.append(p.getRect())

        return hitBoxes
