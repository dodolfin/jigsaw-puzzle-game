from menu import MainMenu

from parameters import SCREEN_SIZE

import pygame
import sys
import os


def run():
    pygame.init()
    pygame.font.init()
    pygame.mixer.music.load(os.path.join('media', 'sound', 'click.ogg'))
    screen = pygame.display.set_mode(SCREEN_SIZE)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    pygame.display.set_icon(pygame.image.load('icon.png'))
    pygame.display.set_caption('Jigsaw Puzzle', 'Jigsaw')

    MainMenu(screen)
    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    run()
