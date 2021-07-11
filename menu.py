from game import Game

from tkinter import *
from tkinter import filedialog, messagebox

from dwidgets import *

import pygame

import os


def dummy():
    pass


class MainMenu:
    def __init__(self, screen):
        self.screen = screen

        self.excursion = Button('Режим «Экскурсия»', (10, 10), self.start_excursion)
        self.new_game = Button('Обычная игра',
                               (10, self.excursion.rect.bottom + 10), self.start_game)
        self.settings = Button('Настройки',
                               (10, self.new_game.rect.bottom + 10), self.start_settings)
        self.quit = Button('Выйти из игры',
                           (10, self.settings.rect.bottom + 10), self.quit_game)

        self.state = 0

        self.mainloop()

    def mainloop(self):
        while self.state == 0:
            self.draw()
            self.events()
            pygame.time.wait(5)

    def draw(self):
        self.screen.fill(WHITE)
        self.excursion.draw(self.screen)
        self.new_game.draw(self.screen)
        self.settings.draw(self.screen)
        self.quit.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            self.excursion.events(event)
            self.new_game.events(event)
            self.settings.events(event)
            self.quit.events(event)

    def start_game(self):
        NewGameSettings(self.screen, self)

    def start_excursion(self):
        Gallery(self.screen, self)

    def start_settings(self):
        Settings(self.screen, self)

    def quit_game(self):
        self.state = -1


class NewGameSettings:
    def __init__(self, screen, menu, filename=None, win_message='Поздравляем! Вы собрали паззл!'):
        self.screen = screen
        self.menu = menu
        self.filename = filename
        self.win_message = win_message

        self.width = 4
        self.height = 4

        self.width_elem = [Button('Кусков по горизонтали: {}'.format(self.width), (10, 10))]
        self.width_elem.append(Button(' − ', (self.width_elem[0].rect.right + 10, 10), self.decr_width))
        self.width_elem.append(Button(' + ', (self.width_elem[1].rect.right + 10, 10), self.incr_width))
        self.height_elem = [
            Button('Кусков по вертикали: {}'.format(self.height), (10, self.width_elem[0].rect.bottom + 10))]
        self.height_elem.append(
            Button(' − ', (self.height_elem[0].rect.right + 10, self.width_elem[0].rect.bottom + 10), self.decr_height))
        self.height_elem.append(
            Button(' + ', (self.height_elem[1].rect.right + 10, self.width_elem[0].rect.bottom + 10), self.incr_height))

        self.back = Button('Назад', (10, self.height_elem[0].rect.bottom + 10), self.stop)
        self.ok = Button('OK', (self.back.rect.right + 10, self.height_elem[0].rect.bottom + 10), self.start_game)

        self.state = 0
        self.mainloop()

    def mainloop(self):
        while self.state == 0:
            self.draw()
            self.events()
            pygame.time.wait(5)

    def draw(self):
        self.screen.fill(WHITE)
        for i in self.width_elem:
            i.draw(self.screen)
        for i in self.height_elem:
            i.draw(self.screen)
        self.back.draw(self.screen)
        self.ok.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
                self.menu.quit_game()
            for i in range(1, 3):
                self.width_elem[i].events(event)
            for i in range(1, 3):
                self.height_elem[i].events(event)
            self.back.events(event)
            self.ok.events(event)

    def decr_width(self):
        self.width -= 1
        if self.width <= 2:
            self.width = 3
        self.update_width()

    def incr_width(self):
        self.width += 1
        if self.width >= 15:
            self.width = 15
        self.update_width()

    def update_width(self):
        self.width_elem[0].update(label='Кусков по горизонтали: {}'.format(self.width))
        for i in range(1, 3):
            self.width_elem[i].update(pos=(self.width_elem[i - 1].rect.right + 10, 10))

    def decr_height(self):
        self.height -= 1
        if self.height <= 2:
            self.height = 3
        self.update_height()

    def incr_height(self):
        self.height += 1
        if self.height >= 15:
            self.height = 15
        self.update_height()

    def update_height(self):
        self.height_elem[0].update(label='Кусков по вертикали: {}'.format(self.height))
        for i in range(1, 3):
            self.height_elem[i].update(
                pos=(self.height_elem[i - 1].rect.right + 10, self.width_elem[0].rect.bottom + 10))

    def stop(self):
        self.state = -1

    @staticmethod
    def select_file():
        root = Tk()
        root.withdraw()
        filename = filedialog.askopenfilename()
        root.destroy()
        return filename

    def greetings(self):
        root = Tk()
        root.withdraw()
        messagebox.showinfo('Победа!', self.win_message)
        root.destroy()

    def start_game(self):
        self.stop()

        if not self.filename:
            self.filename = NewGameSettings.select_file()

        state = Game(self.screen, self.filename, self.menu, self.height, self.width).mainloop()
        if state == -1:
            self.greetings()


class Gallery:
    def __init__(self, screen, menu):
        self.screen = screen
        self.menu = menu

        self.paintings = [
            ImageButton(os.path.join('media', 'image', '.picasso', 'g2_preview.jpg'),
                        (300, 200), (5, 5), self.g2)]
        self.paintings.append(ImageButton(os.path.join('media', 'image', '.picasso', 'g3_preview.jpg'), (300, 200),
                                          (self.paintings[0].rect.right + 5, 5), self.g3))
        self.paintings.append(ImageButton(os.path.join('media', 'image', '.picasso', 'g6_preview.jpg'), (300, 200),
                                          (5, self.paintings[0].rect.bottom + 5), self.g6))

        self.back = Button('Назад', (5, self.paintings[2].rect.bottom + 5), self.stop)

        self.state = 0
        self.mainloop()

    def mainloop(self):
        while self.state == 0:
            self.events()
            self.draw()

    def stop(self):
        self.state = -1

    def events(self):
        for event in pygame.event.get():
            for i in self.paintings:
                i.events(event)
            self.back.events(event)

    def draw(self):
        self.screen.fill(WHITE)
        for i in self.paintings:
            i.draw(self.screen)
        self.back.draw(self.screen)
        pygame.display.flip()

    def g2(self):
        NewGameSettings(self.screen, self.menu, os.path.join('media', 'image', '.picasso', 'g2.jpg'),
                        '«Семейство комедиантов», 1905. Эта картина относится к розовому периоду Пикассо. Некоторые искусствоведы считают, что это завуалированное изображение Пикассо и его круга, члены которого бедны, но независимы друг от друга.')

    def g3(self):
        NewGameSettings(self.screen, self.menu, os.path.join('media', 'image', '.picasso', 'g3.jpg'),
                        '«Голубь мира», 1961. Первый вариант этого рисунка Пикассо сделал ещё в 1949 году. Рисунок получил известность как эмблема Конгресса сторонников мира (первое собрание прошло в 1949 году), но голубь мира существовал и раньше: в библейском сюжете белый голубь приносит Ною в ковчег ветвь маслины.')

    def g6(self):
        NewGameSettings(self.screen, self.menu, os.path.join('media', 'image', '.picasso', 'g6.jpg'),
                        '«Натюрморт с черной головой быка», 1938.')


class Settings:
    def __init__(self, screen, menu):
        self.screen = screen
        self.menu = menu

        self.volume = pygame.mixer.music.get_volume()

        self.sound = Button('Звук включён', (10, 10), self.change)

        if self.volume < 1e-8:
            self.sound.update(label='Звук выключен')

        self.back = Button('Назад', (10, self.sound.rect.bottom + 10), self.stop)

        self.state = 0
        self.mainloop()

    def mainloop(self):
        while self.state == 0:
            self.draw()
            self.events()
            pygame.time.wait(5)

    def draw(self):
        self.screen.fill(WHITE)
        self.sound.draw(self.screen)
        self.back.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
                self.menu.quit_game()
            self.sound.events(event)
            self.back.events(event)

    def change(self):
        if self.volume < 1e-8:
            self.volume = 1.0
            self.sound.update(label='Звук включён')
        else:
            self.volume = 0.0
            self.sound.update(label='Звук выключен')
        pygame.mixer.music.set_volume(self.volume)

    def stop(self):
        self.state = -1
