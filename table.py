from parameters import *
import pygame


class Table:
    background = None

    def __init__(self, background='#ffffff'):
        if background[0] == '#':
            Table.background = pygame.Surface(SCREEN_SIZE, flags=pygame.SRCALPHA)
            Table.background.fill(pygame.Color(background))
        else:
            Table.background = pygame.image.load(background)
            Table.background.convert_alpha()

        filler = pygame.Surface(PUZZLE_SIZE, flags=pygame.SRCALPHA)
        filler.fill(SHADOW_COLOR)
        Table.background.blit(filler, (BORDER_SIZE, BORDER_SIZE))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
