import pygame
import random
from Wall import Wall
from Constants import *

class maze:
    #   Margins on the sides. In case they need to be differnet
    margin_top = 50
    margin_left = 50
    margin_right = 50
    margin_bottom = 50

    #   Idea: A block is an empty square component of a maze alongwith a wall. The wall's longer side is the length of the block 

    #   The number of blocks in a maze is decided automatically by calculating how many fit in.
    n_x = (WIDTH//2 - margin_left - margin_right - WALL_THICKNESS)//(BLOCK_SIZE + WALL_THICKNESS)   #   The number of blocks in x-axis of maze
    n_y = (HEIGHT - margin_top - margin_bottom - WALL_THICKNESS)//(BLOCK_SIZE + WALL_THICKNESS)     #    The number of blocks in y-axis of maze
    
    w = n_x * (BLOCK_SIZE + WALL_THICKNESS) + WALL_THICKNESS                #   The width of 1 block
    h = n_y * (BLOCK_SIZE + WALL_THICKNESS) + WALL_THICKNESS                #   The height of 1 block

    pixels_x = (WALL_THICKNESS + (BLOCK_SIZE + WALL_THICKNESS) * n_x )      #   Number of pixels in x-axis of 1 maze
    pixels_y = (WALL_THICKNESS + (BLOCK_SIZE + WALL_THICKNESS) * n_y)       #   Number of pixels in y-axis of 1 maze

    walls = []      #   Stores all the walls 
    array = []      #   An array of all the pixels of a maze that stores 0 for wall, 1 for empty path, 100 for final destination.

    def __init__(self, text, FONT, offset):
        self.offset = offset        #   Helps make replicas. This is the horizontal offset since our game has only 2 windows
        self.rect = pygame.Rect(maze.margin_left + offset, maze.margin_top, maze.w, maze.h)

        #   Destination
        self.end_point = (self.rect.right - WALL_THICKNESS//2, self.rect.bottom - WALL_THICKNESS - BLOCK_SIZE//2)
        self.end_rect = pygame.Rect(0, 0, WALL_THICKNESS, BLOCK_SIZE)
        self.end_rect.center = self.end_point

        #   Start
        self.start_point = (self.rect.left + WALL_THICKNESS//2, self.rect.top + WALL_THICKNESS + BLOCK_SIZE//2)
        self.start_rect = pygame.Rect(0, 0, WALL_THICKNESS, BLOCK_SIZE)
        self.start_rect.center = self.start_point

        #   Name of Maze
        self.text = FONT.render(text, 1, TEXT_COLOR)

    #   Makes all possible walls inside a maze
    def initialize_walls():
        last_x = maze.margin_left
        last_y = maze.margin_top
        for i in range(maze.n_x+1):
            for j in range(maze.n_y+1):
                if i != maze.n_x:
                    maze.walls.append(Wall(last_x, last_y, 0))
                    maze.walls[-1].set_index(i, j)

                if j != maze.n_y and (i,j) != (0,0) and (i,j) != (maze.n_x, maze.n_y-1): 
                    maze.walls.append(Wall(last_x, last_y, 1))
                    maze.walls[-1].set_index(i, j)

                last_y += (BLOCK_SIZE + WALL_THICKNESS)
            last_y = maze.margin_top
            last_x += (BLOCK_SIZE + WALL_THICKNESS)

    '''
    A bunch of blocks or squares define the path and a bunch of thin rectangles are walls

    Maze Generation
    - Start off with all possible walls. Shuffle it. 
    - Iterate over the walls and remove them if blocks on either sides are in disjoint sets
    - Unite all disjoint sets and ignore wall if two blocks are in same set
    - Draw maze

    Note that track of parent sets will be maintained for individual blocks.
    '''

    #   The use of DSU (Disjoint Set Union) helps make a valid maze
    parent_set = [i for i in range(n_x * n_y)]

    #   Returns parent of set
    def find_parent(i):
        if i != maze.parent_set[i]:
            maze.parent_set[i] = maze.find_parent(maze.parent_set[i])
        return maze.parent_set[i]

    #   Merges 2 sets into 1. 
    def merge_sets(a, b):
        if maze.find_parent(a) == maze.find_parent(b): return

        #   Ensures all sets are merged with the starting set
        if maze.parent_set[a] == 0:
            maze.parent_set[maze.parent_set[b]] = 0
        else:
            maze.parent_set[maze.parent_set[a]] = maze.parent_set[b]

    def generate_maze():
        #   Shuffles all the walls. This is the single reason the maze is random every single time. A single permutation of walls will lead to the same maze every time
        random.shuffle(maze.walls)

        # Generates the entire maze
        for i in range(len(maze.walls)):
            maze.check_one_wall(i)

    #   Checks if keeping the wall is possible without making a closed path inside the maze. If it isn't, it hides the wall
    def check_one_wall(k):
        if k >= len(maze.walls): return
        
        wall = maze.walls[k]
        k += 1

        i,j = wall.get_index()

        #   Return if this is the outer wall of the maze since we want to keep all of them
        if wall.vertical: 
            if (i == 0 or i == maze.n_x): return
        elif j == 0 or j == maze.n_y: return

        #   a, b are the 2 blocks on the 2 sides of the wall.
        a = maze.n_x * j + i
        if not wall.vertical:
            b = a - maze.n_x
        else:
            b = a-1

        #   If it is possible to reach a from b despite keeping this wall, keep it. Else remove it.
        if maze.find_parent(a) == maze.find_parent(b): return
        maze.merge_sets(a, b)
        wall.visible = 0

    #   Draws the entire maze
    def draw(self, WINDOW):
        pygame.draw.rect(WINDOW, MAZE_COLOR, self.rect)
        pygame.draw.rect(WINDOW, START_COLOR, self.start_rect)
        pygame.draw.rect(WINDOW, END_COLOR, self.end_rect)
        WINDOW.blit(self.text, (self.rect.left, self.rect.top - FONT_SIZE))
        
        for i in maze.walls:
            if i.visible:
                i.draw(WINDOW, WALL_COLOR, self.offset)

    #   Generates the array of the maze
    def generate_array():
        #   1 = normal pathway
        maze.array = [[1 for i in range(maze.pixels_x)] for i in range(maze.pixels_y)] 

        #   0 = forbidden / wall 
        for wall in maze.walls:
            if wall.visible == 0: continue

            (x1,y1), (x2,y2) = wall.get_bounds()
            for i in range(x1, x2):
                for j in range(y1, y2):
                    maze.array[j - maze.margin_top][i - maze.margin_left] = 0 

        for j in range(BLOCK_SIZE):
            maze.array[maze.margin_top + WALL_THICKNESS + j][0] = 0     #   to make sure player stays inside maze
            maze.array[maze.pixels_y - WALL_THICKNESS - j][-1] = 100    #   100 = endpoint

    #   I didn't need to use this:  Could have helped in implementing some additional things
    def initialize_array(self):
        self.array = maze.array