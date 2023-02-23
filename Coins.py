import pygame

pygame.font.init()
myFont = pygame.font.SysFont('Comic Sans MS', 23) #load a font for use

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.color = (255, 255, 0)


    def getCollisionRect(self):
        return pygame.Rect(self.x-19, self.y-19, self.size + 8, self.size + 8)

    def changeColor(self, color):
        self.color = color

    def draw(self, screen, num):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 20.0, 0)
        # pygame.draw.rect(screen, (255, 0, 0), self.getCollisionRect(), 1)
        textSurface = myFont.render(f'{num}', True, (0, 0, 0))
        screen.blit(textSurface, (self.x-7, self.y-16))

