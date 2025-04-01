import pygame
from Constants import *

#   A wall is a basic component of a maze. A bunch of Walls make a maze.
class Wall:
    def __init__(self, x, y, vertical):
        self.visible = 1            #   Walls that are removed are just invisible
        self.x = x
        self.y = y

        self.vertical = vertical    #   Tells whether wall is vertical or horizontal
        if vertical: 
            self.w = WALL_THICKNESS
            self.h = BLOCK_SIZE + 2*WALL_THICKNESS
        else:
            self.w = BLOCK_SIZE + 2*WALL_THICKNESS
            self.h = WALL_THICKNESS
        self.rect = pygame.Rect(x, y, self.w, self.h)
        
        self.i = -1
        self.j = -1

    #   The index of a wall is used to identify it among the grid of walls
    def set_index(self, i, j):
        self.i = i
        self.j = j
    
    def get_index(self):
        return (self.i, self.j)

    def get_size(self):
        return (self.w, self.h)

    def get_coord(self):
        return (self.x, self. y)

    def get_bounds(self):
        return ((self.x, self.y), (self.x + self.w, self.y + self.h))
    
    #   Draws the wall
    def draw(self, WIN, COLOR, offset_x):
        self.rect.x += offset_x
        pygame.draw.rect(WIN, COLOR, self.rect)
        self.rect.x -= offset_x