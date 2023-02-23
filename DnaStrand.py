import random as rand
import time

from Player import *

class PlayerAI:

    count = 400

    def __init__(self):
        self.player = Player((rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255)))
        self.strand = []
        self.createSequence()
        self.delay = 100_000_000
        self.currentIndex = 0
        self.nextAct = time.time_ns() + self.delay
        self.x_distance_covered = 0

    def get_score(self):
        return (self.player.get_score() * 350) + self.x_distance_covered

    def get_current_allele(self):
        return self.currentIndex

    def is_done(self):
        return self.currentIndex == self.count

    def reset(self):
        self.currentIndex = 0
        self.player.captured_coins = [False for i in range(len(self.player.map.coins))]
        self.player.set_x(400)
        self.player.set_y(400)

    def createSequence(self):
        for i in range(self.count):
            choice = rand.randint(1, 100)
            if choice <= 80:
                self.strand.append(0)
            elif choice <= 86:
                self.strand.append(1)
            elif choice <= 93:
                self.strand.append(2)
            elif choice <= 100:
                self.strand.append(3)

    def act(self):
        # print(str(time.time_ns()))
        if self.nextAct < time.time_ns() and self.currentIndex < self.count:
            if self.strand[self.currentIndex] == 1:
                self.player.jump()
            elif self.strand[self.currentIndex] == 2:
                self.player.stepLeft()
            elif self.strand[self.currentIndex] == 3:
                self.player.stepRight()
            self.nextAct = time.time_ns() + self.delay
            # print(str(self.currentIndex) + ":" + str(self.strand[self.currentIndex]))
            self.currentIndex += 1
            self.x_distance_covered = self.player.x - 400

        return self.player.step()

    def draw(self, screen):
        self.player.draw(screen)

    def setMap(self, map):
        self.player.setMap(map)

    def setDNA(self, dna):
        self.strand = dna