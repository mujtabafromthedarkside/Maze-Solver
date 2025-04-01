import copy
import random
from Dot import Dot
from Brain import Brain
from Constants import *

#   A population consists of many dots
class Population:
    def __init__(self, size):
        self.dots = [Dot() for i in range(size)]
        self.bestDot = 0        #   stores index of best dot
        self.pref_sums = [0]    #   stores prefix sums of fitness scores of all dots. This is useful in SelectParent()

    #   Draws the whole population
    def draw(self, WINDOW):
        for i in range(len(self.dots)):
            self.dots[i].draw(WINDOW)

    #   Updates all dots
    def update(self):
        for i in range(len(self.dots)):
            self.dots[i].update()

    #   Checks if all dots have stopped moving
    def allDead(self):
        none_lingering = 1      #   True means all dots have either reached end or hit wall
        all_hitWall = 1         #   True means all dots have hit wall
        for i in range(len(self.dots)):
            #   If any dot is moving
            if not self.dots[i].dead and not self.dots[i].reached and not self.dots[i].hitWall: return 0

            if self.dots[i].dead: none_lingering = 0
            if not self.dots[i].hitWall: all_hitWall = 0
            
        return all_hitWall + none_lingering + 1
    
    #   Passing on the brain from one generation to the next
    def natural_selection(self):
        self.calculatePrefSums()

        newDots = []

        for i in range(1, len(self.dots)):
            newDots.append(self.selectParent().getBaby())
        newDots.append(self.dots[self.bestDot].getBaby())
        newDots[-1].isBest = True

        self.dots = newDots

    #   returns a parent dot through the probability based on fitness scores
    def selectParent(self):
        #   A random number between 0 and total fitness sum
        rnd = random.uniform(0, self.pref_sums[-1])
        while rnd == 0:
            rnd = random.uniform(0, self.pref_sums[-1])

        #   Binary search through the prefix sums array to find the upperbound index.
        #   The idea of this is basically: The one with higher fitness score has higher chance to spawn a random number inside its prefix sum
        l = 1
        r = len(self.dots)
        while l <= r:
            mid = l + (r-l)//2
            if rnd == self.pref_sums[mid]:
                l = mid; break
            elif rnd < self.pref_sums[mid]: r = mid - 1
            else: l = mid + 1
        l -= 1
        return self.dots[l]

    def calculatePrefSums(self):
        self.pref_sums = [0]
        for i in range(len(self.dots)):
            self.pref_sums.append(self.pref_sums[-1] + self.dots[i].fitness)

    #   Mutates the brains of all dots except the best dot
    def mutate(self):
        self.BestDot()
        for i in range(len(self.dots)):
            if not self.dots[i].isBest:
                self.dots[i].brain.mutate()

    #   Finds the dot with highest score and saves its index
    def BestDot(self):
        mx = 0.0
        self.bestDot = 0

        for i in range(len(self.dots)):
            if self.dots[i].fitness > mx:
                mx = self.dots[i].fitness
                self.bestDot = i