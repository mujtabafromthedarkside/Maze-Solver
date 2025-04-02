import pygame
from Maze import maze
from Population import Population
from Dot import Dot
from Brain import Brain
from Constants import *
import threading

#   Sets up the window and font style
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
pygame.font.init()
FONT = pygame.font.SysFont(TEXT_FONT, FONT_SIZE)

#   setting up the ID for a specific event
REACHED_END = pygame.USEREVENT + 1

#   Setting up the mazes
maze_player = maze('Player', FONT, 0)
maze_bot = maze('Bot (Dots: ' + str(NUMBER_OF_DOTS) + ')', FONT, WIDTH//2)
maze.initialize_walls()
maze.generate_maze()
maze.generate_array()

#   Defining some static attributes for dot.
Dot.startx = maze_bot.start_rect.right
Dot.starty = maze_bot.start_rect.center[1] - Dot.h//2
Dot.goal = maze_bot.end_rect

player = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
clock = pygame.time.Clock()                 #   For FPS
running = True                              #   If False, window closes
keep_playing = 1                            #   If True, player can keep moving.

pop = Population(NUMBER_OF_DOTS)            #   Initializes population of dots
generation_num = 1                          #   Keeps track of the generation
stepNum = 0                                 #   Keeps track of the step number at any moment

def update_population():
    global pop, generation_num, stepNum, running
    clock2 = pygame.time.Clock()                 #   For FPS
    
    while running:
        state = pop.allDead()
        clock2.tick(FPS)
        
        if state: stepNum = 0                   #   state = 0 means dots are still moving, else next generation begins and steps are reset
        if state == 1:                          #   state = 1 means some dots still had steps left, so we can safely increase steps
            Brain.stepCount += DELTA_STEP
            Brain.stepCount = min(Brain.stepCount, STEPS_LIMIT)

        if state == 3:                          #   state = 3 means all dots have hit the wall and died in which case we can't do natural selection
            Brain.stepCount = INITIAL_STEP_COUNT
            pop = Population(NUMBER_OF_DOTS)
            generation_num = 1
        elif state:
            pop.mutate()                        #   mutates the brains of current population while leaving the best one as it is
            pop.natural_selection()             #   from the current population, selects parents based on fitness. 
            generation_num += 1
        pop.update()                            #   Updates motion of population

def update_player():
    global keep_playing, player
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_RETURN]:       #   if Enter key was pressed, Reset the game.
        keep_playing = 1
        player.center = maze_player.start_rect.center
        player.left = maze_player.start_rect.right
    if keep_playing: movement_player(keys_pressed, player)

def main():
    #   Player rectangle's starting point
    global player, keep_playing, running, stepNum
    player.center = maze_player.start_rect.center
    player.left = maze_player.start_rect.right

    pop_thread = threading.Thread(target=update_population)  #   Thread for updating population
    pop_thread.start()

    while running:
        clock.tick(FPS)                         #   ensures FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:       #   If the cross on top right corner is clicked, quit
                running = False
            
            if event.type == REACHED_END:       #   Triggered if player reaches the end
                keep_playing = 0

        update_player()

        draw_window(player, not keep_playing, pop, generation_num, stepNum)
        stepNum += 1

    pop_thread.join()  #   Wait for the population thread to finish

    # Outside Loop. Quit Window
    pygame.quit()

#   Draws all the components and updates the display
def draw_window(player, write_win_text, population, generation, steps):

    #   Maze
    WINDOW.fill(WINDOW_COLOR)
    maze_player.draw(WINDOW)  
    maze_bot.draw(WINDOW)
    
    #   Player
    pygame.draw.rect(WINDOW, PLAYER_COLOR, player)

    #   Player Text
    if write_win_text: write_text_center('GAME OVER!!', maze_player.rect.center, BLACK)
    write_text_center('Press Enter to Reset', (maze_player.rect.center[0], maze_player.rect.bottom + FONT_SIZE//2))

    #   Dots
    population.draw(WINDOW)

    #   Dots Text
    write_text('Generation #: ' + str(generation), (maze_bot.rect.left, maze_bot.rect.bottom))
    write_text('# Steps: ' + str(steps), (maze_bot.rect.center[0], maze_bot.rect.bottom))

    #   Update Display
    pygame.display.update()

#   Writes given text where the given coordinates will be the center of the text.
def write_text_center(wanna_print, center, text_color=TEXT_COLOR):
    text = FONT.render(wanna_print, True, text_color)
    x = center[0] - text.get_rect().width//2
    y = center[1] - text.get_rect().height//2
    WINDOW.blit(text, (x, y))

#   Writes given text where the given coordinates will be the topleft corner of the text.
def write_text(wanna_print, topleft_corner):
    text = FONT.render(wanna_print, True, TEXT_COLOR)
    WINDOW.blit(text, topleft_corner)

#   Applies checks for the movement of the player.  Moves the player in direction given by input keys. Checks if there is a wall, it stops.
def movement_player(keys_pressed, player):
    if keys_pressed[pygame.K_UP]:
        for i in range(1, PLAYER_VELOCITY+1):
            safe = 1

            for j in range(player.left, player.right):
                if maze.array[player.top - 1 - maze.margin_top][j - maze.margin_left] == 0:
                    safe = 0
                    break
            
            if safe: player.y -= 1
            else: break
    
    if keys_pressed[pygame.K_DOWN]:
        for i in range(1, PLAYER_VELOCITY+1):
            safe = 1

            for j in range(player.left, player.right): 
                if maze.array[player.bottom + 1 - maze.margin_top - 1][j - maze.margin_left] == 0: 
                    safe = 0
                    break
            
            if safe: player.y += 1
            else: break
    
    if keys_pressed[pygame.K_LEFT]:
        for i in range(1, PLAYER_VELOCITY+1):
            safe = 1           
            
            for j in range(player.top, player.bottom):
                if maze.array[j - maze.margin_top][player.left - maze.margin_left - 1] == 0: 
                    safe = 0
                    break

            if safe: player.x -= 1
            else: break
    
    found = 0
    if keys_pressed[pygame.K_RIGHT]:
        for i in range(1, PLAYER_VELOCITY+1):
            safe = 1           
            
            for j in range(player.top, player.bottom):
                if maze.array[j - maze.margin_top][player.right - 1 - maze.margin_left + 1] == 100:
                    found = 1
                    break
                if maze.array[j - maze.margin_top][player.right - 1 - maze.margin_left + 1] == 0: 
                    safe = 0
                    break

            if found: 
                pygame.event.post(pygame.event.Event(REACHED_END))
                return
            if safe: player.x += 1
            else: break

if __name__ == '__main__':
    main()
