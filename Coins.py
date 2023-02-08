import pygame

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30


    def getCollisionRect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.getCollisionRect())
