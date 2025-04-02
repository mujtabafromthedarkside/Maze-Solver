'''
This is the place you wanna be for customizing the game
Note that tweaking the properties of the dots will really matter in improving the effectiveness of the genetic algorithm
'''

#   Common Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 111, 255)
ORANGE = (255, 128, 0)
PURPLE = (128, 0, 255)
YELLOW = (255, 255, 0)
GREY = (143, 143, 143)
BROWN = (186, 127, 50)
DARK_GREEN = (0, 128, 0)
DARKER_GREEN = (0, 50, 0)
DARK_BLUE = (0, 0, 128)

#   Assigned Colors. Change from here to customize the visuals. I think the names are self-explanatory
WINDOW_COLOR = PURPLE
TEXT_COLOR = WHITE
MAZE_COLOR = WHITE
WALL_COLOR = ORANGE
START_COLOR = BLUE
END_COLOR = RED
PLAYER_COLOR = PURPLE
HITWALL_COLOR =  GREY
REACHED_COLOR =  BLUE
BEST_DOT_COLOR =  RED
DOT_COLOR = BLACK

#   Properties of Display Window
WINDOW_TITLE = 'Maze Game'  #   The title that appears on top of the window
FPS = 60                    #   Frames per second
WIDTH, HEIGHT = 1280, 720   #   Width and Height of the Window that the game runs on
TEXT_FONT = 'calibri'       #   Decides the font to use. 
FONT_SIZE = 30              #   Font size for the text displayed

#   Properties of Maze
BLOCK_SIZE = 50             #   A block is another basic component besides a wall. A block represents the empty space. Making this smaller makes the maze more complicated
WALL_THICKNESS = 10         #   DO NOT MAKE THIS THINNER THAN VELOCITY_LIMTT
MAZE_BOT_OFFSET = WIDTH//2  #   DO NOT CHANGE THIS. This helps since I need to just replicate the player maze for the bot maze and offset it by some horizontal distance, here being half the window width

#   Properties of Player
PLAYER_WIDTH = 20           #   Width of Player's rectangle
PLAYER_HEIGHT = 20          #   Height of Player's rectangle
PLAYER_VELOCITY = 3         #   Player velocity is a constant number unlike the dots

#   Properties of Dots
NUMBER_OF_DOTS = 1000       #   Total number of dots. The more the better but we can only compute steps for so many :)
DOT_WIDTH = 4               
DOT_HEIGHT = 4
VELOCITY_LIMIT = 7          #   DO NOT MAKE THIS GREATER THAN WALL_THICKNESS. Max Bot Velocity. 
RATE_OF_MUTATION = 0.001    #   Probability of mutation
INITIAL_STEP_COUNT = 50     #   Starting steps count
DELTA_STEP = 25             #   Increase in steps with each iteration. Increasing increases randomness and thus more chance to find path, but too much increase just means they all die.
STEPS_LIMIT = 2500          #   Steps max out at this number