import pygame
from vector import vector
from Brain import Brain
from Maze import maze
from Constants import *

class Dot:
    w = DOT_WIDTH
    h = DOT_HEIGHT
    goal = None     
    def __init__(self):
        self.rect = pygame.Rect(Dot.startx, Dot.starty, Dot.w, Dot.h)       # This rectangle will be used to move the dot
        self.vel = vector(0,0)      # velocity
        self.acc = vector(0,0)      # acceleration

        self.brain = Brain(Brain.stepCount)     # forces being applied
        self.fitness = 0.0          # score which decides the probability of cloning
        self.dead = False           # True if dot has completed its number of steps for current generation
        self.reached = False
        self.hitWall = False
        self.isBest = False

    #   draws the dot in different colors depending on the state of the dot
    def draw(self, WINDOW):
        if self.hitWall: color = HITWALL_COLOR
        elif self.reached: color = REACHED_COLOR
        elif self.isBest: color = BEST_DOT_COLOR
        else: color = DOT_COLOR
        pygame.draw.rect(WINDOW, color, self.rect)

    def move(self):
        #   If steps are still left, move
        if len(self.brain.directions) > self.brain.steps:
            self.acc = self.brain.directions[self.brain.steps]
            self.brain.steps += 1

        #   No steps left. Dot is Dead
        else:
            self.dead = True
            return

        #   Moves the dot and limits its velocity
        self.vel.add(self.acc)
        self.vel.limit(VELOCITY_LIMIT)
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

    #   Applies some checks before moving the dot and recalculates some states upon moving
    def update(self):
        if not self.dead and not self.reached and not self.hitWall:
            self.move()

            if self.isColliding(): self.hitWall = True
            elif self.rect.colliderect(Dot.goal): self.reached = True
            self.calculateFitness()

    #   This returns the fitness score that decides probability of being passed on
    def calculateFitness(self):
        x1, y1 = self.rect.topleft
        x2, y2 = Dot.goal.center
        dist = vector.dist(x1, y1, x2, y2)

        #   Both distance from end goal and # steps are used to calculate fitness
        if self.dead or self.reached:
            self.fitness = 1.0 / (dist**2 + self.brain.steps**2)
        else:
            self.fitness = 0.00000000000001

    #   Returns true if dot is colliding with any of the maze walls 
    def isColliding(self):
        #   Checks if the dot went out of the maze
        if self.rect.top < maze.margin_top + WALL_THICKNESS or self.rect.right > WIDTH - maze.margin_right - WALL_THICKNESS or self.rect.left < MAZE_BOT_OFFSET + maze.margin_left + WALL_THICKNESS or self.rect.bottom > maze.h + maze.margin_top - WALL_THICKNESS: return True
        
        #   Checks are applied on each of the dot's borders. Checking the whole border becomes really important in case of larger dots
        #   Checks left, right borders
        for j in range(self.rect.left, self.rect.right):
            if maze.array[self.rect.top - maze.margin_top][j - maze.margin_left - MAZE_BOT_OFFSET] == 0: return 1
            elif maze.array[self.rect.bottom - maze.margin_top - 1][j - maze.margin_left - MAZE_BOT_OFFSET] == 0: return 1
        
        #   Checks top, bottom borders
        for j in range(self.rect.top, self.rect.bottom):
            if maze.array[j - maze.margin_top][self.rect.left - maze.margin_left - MAZE_BOT_OFFSET] == 0: return 1
            elif maze.array[j - maze.margin_top][self.rect.right - 1 - maze.margin_left - MAZE_BOT_OFFSET] == 0: return 1
        return 0

    #   returns a new dot with the same brain
    def getBaby(self):
        baby = Dot()
        baby.brain = self.brain.clone()
        
        return baby
        

