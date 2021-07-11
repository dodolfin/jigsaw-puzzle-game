from styles import DefaultStyle
from parameters import *

from table import Table
from puzzle import Jigsaw

from tkinter import filedialog
from tkinter import *

from dwidgets import *

import pygame


class Game:
    def __init__(self, screen, filename, menu, height, width):
        super().__init__()

        self.screen = screen
        self.table = Table()

        self.menu = menu

        image = open(filename, mode='rb')
        self.puzzle = Jigsaw(image, width, height)
        image.close()

        self.state = 0

        self.pause = Button('Пауза', (10, 10), self.pause_screen)

    def mainloop(self):
        while self.state == 0:
            self.events()
            self.drawing()

            if self.check_victory():
                self.state = -1
                # self.afterparty()

            pygame.time.wait(5)
        return self.state

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = -2
                self.menu.quit_game ()
            elif event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                self.pause.events(event)
                self.puzzle.events(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_screen()

    def drawing(self):
        self.table.draw(self.screen)
        self.puzzle.draw(self.screen)
        self.pause.draw(self.screen)
        pygame.display.flip()

    @staticmethod
    def check_victory():
        return Jigsaw.check_victory()

    def pause_screen(self):
        PauseScreen(self.screen, self)

    def stop_game(self):
        self.state = -2


class PauseScreen:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

        self.resume = Button('Продолжить', (10, 10), self.stop)
        self.quit = Button('Выйти в главное меню',
                           (10, self.resume.rect.bottom + 10), self.stop_game)

        self.state = 0

        self.mainloop()

    def mainloop(self):
        self.pre_draw()
        while self.state == 0:
            self.draw()
            self.events()
            pygame.time.wait(5)

    def pre_draw(self):
        filler = pygame.Surface(SCREEN_SIZE, flags=pygame.SRCALPHA)
        filler.fill(SHADOW_COLOR)
        self.screen.blit(filler, (0, 0))

    def draw(self):
        self.resume.draw(self.screen)
        self.quit.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = -1
                self.game.stop_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stop()
            self.resume.events(event)
            self.quit.events(event)

    def stop(self):
        self.state = -1

    def stop_game(self):
        self.state = -1
        self.game.stop_game()
