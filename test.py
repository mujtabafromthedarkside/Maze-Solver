import pygame
from Constants import *
r = pygame.Rect(0,0,4,4)
r.x += 57.9238
H,W = 1280, 720
WIN = pygame.display.set_mode((H,W))
WINDOW_COLOR = WHITE
FPS = 60

def draw_window():
    WIN.fill(WINDOW_COLOR)

    pygame.draw.rect(WIN, BLACK, r)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()
        draw_window()
        
    pygame.quit()

if __name__ == '__main__':
    main()

