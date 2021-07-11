from styles import *

import pygame


class Button:
    def __init__(self, label, pos, f=None):
        self.style = DefaultStyle
        self.label = label
        self.pos = pos

        self.surface = self.render()

        self.rect = self.surface.get_rect().move(self.pos[0], self.pos[1])

        self.state = 0
        self.f = f

    def render(self):
        font = pygame.font.SysFont(self.style.font_name, self.style.font_size)
        label_size = font.size(self.label)
        surface = pygame.Surface((label_size[0] + 2 * self.style.padding,
                                  label_size[1] + 2 * self.style.padding))

        surface.fill(self.style.background_color)
        pygame.draw.rect(surface, self.style.border_color, surface.get_rect(), self.style.border_width)
        surface.blit(font.render(self.label, True, self.style.color, self.style.background_color),
                     (self.style.padding, self.style.padding))

        return surface

    def update(self, style=None, pos=None, label=None):
        if style:
            self.style = style

        if pos:
            self.pos = pos

        if label:
            self.label = label

        self.surface = self.render()
        self.rect = self.surface.get_rect().move(self.pos[0], self.pos[1])

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = 2
                self.update(PressedStyle)
        elif event.type == pygame.MOUSEMOTION:
            collide = self.rect.collidepoint(event.pos)
            if collide and self.state == 0:
                self.state = 1
                self.update(HoveredStyle)
            elif not collide:
                self.state = 0
                self.update(DefaultStyle)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.state != 0:
                self.state = 0
                self.update(DefaultStyle)
            if self.rect.collidepoint(event.pos):
                self.f()

    def draw(self, screen):
        screen.blit(self.surface, self.pos)


class ImageButton(Button):
    def __init__(self, filename, size, pos, f=None):
        self.size = size
        self.image = self.scale_image(pygame.image.load(filename))
        self.rect = self.image.get_rect()
        super().__init__('', pos, f)

    def scale_image(self, image):
        return pygame.transform.smoothscale(image, self.size)

    def render(self):
        surface = pygame.Surface((self.size[0] + 2 * self.style.padding,
                                  self.size[1] + 2 * self.style.padding))

        surface.fill(self.style.background_color)
        pygame.draw.rect(surface, self.style.border_color, surface.get_rect(), self.style.border_width)
        surface.blit(self.image, (self.style.padding, self.style.padding))

        return surface
