import pygame
from parameters import *

from random import randint
from math import hypot, fabs


def dist(a, b):
    return hypot(fabs(a[0] - b[0]), fabs(a[1] - b[1]))


class Jigsaw:
    width = None
    height = None

    image = None

    EPS_W = None
    EPS_H = None

    def __init__(self, file, width, height):
        Jigsaw.width = width
        Jigsaw.height = height

        Piece.width = PUZZLE_WIDTH // width
        Piece.height = PUZZLE_HEIGHT // height

        Piece.comp_count = 0

        image = pygame.image.load(file)
        image.convert_alpha()
        Jigsaw.image = Jigsaw.scale_image(image)

        self.pieces = Jigsaw.gen_pieces()

        self.pressed = -1
        Jigsaw.EPS_W = hypot(Jigsaw.width / 2, EPS)
        Jigsaw.EPS_H = hypot(Jigsaw.height / 2, EPS)

    @staticmethod
    def scale_image(image):
        return pygame.transform.smoothscale(image, PUZZLE_SIZE)

    @staticmethod
    def gen_pieces():
        pieces = [None] * (Jigsaw.width * Jigsaw.height)

        for i in range(Jigsaw.height):
            for j in range(Jigsaw.width):
                piece_image = pygame.Surface((Piece.width, Piece.height),
                                             flags=pygame.SRCALPHA)
                piece_image.blit(Jigsaw.image, (0, 0),
                                 (j * Piece.width, i * Piece.height,
                                  Piece.width, Piece.height))

                pieces[i * Jigsaw.width + j] = Piece(
                    i * Jigsaw.width + j,
                    piece_image,
                    (
                        randint(0, SCREEN_WIDTH - Piece.width),
                        randint(0, SCREEN_HEIGHT - Piece.height)
                    )
                )

        for i in range(Jigsaw.height):
            for j in range(Jigsaw.width):
                if (i == 0 and j == 0) or\
                    (i == Jigsaw.height - 1 and j == 0) or\
                    (i == 0 and j == Jigsaw.width - 1) or\
                    (i == Jigsaw.height - 1 and j == Jigsaw.width - 1):
                    pieces[i * Jigsaw.width + j].set_comp()

        return pieces

    def draw(self, screen):
        for piece in self.pieces:
            if piece.comp:
                piece.draw(screen)
        for piece in self.pieces:
            if not piece.comp:
                piece.draw(screen)

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for piece in self.pieces[::-1]:
                if not piece.comp:
                    if piece.rect.collidepoint(event.pos):
                        self.pressed = piece.n
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed != -1:
                cur_piece = self.pieces[self.pressed]
                # Top
                if cur_piece.n // Jigsaw.width != 0:
                    top_piece = self.pieces[cur_piece.n - Jigsaw.width]
                    if top_piece.comp and dist(cur_piece.rect.midtop, top_piece.rect.midbottom) <= Jigsaw.EPS_W:
                        cur_piece.set_comp()

                # Right
                if cur_piece.n % Jigsaw.width != Jigsaw.width - 1:
                    right_piece = self.pieces[cur_piece.n + 1]
                    if right_piece.comp and dist(cur_piece.rect.midright, right_piece.rect.midleft) <= Jigsaw.EPS_H:
                        cur_piece.set_comp()

                # Bottom
                if cur_piece.n // Jigsaw.width != Jigsaw.height - 1:
                    bottom_piece = self.pieces[cur_piece.n + Jigsaw.width]
                    if bottom_piece.comp and dist(cur_piece.rect.midbottom, bottom_piece.rect.midtop) <= Jigsaw.EPS_W:
                        cur_piece.set_comp()

                # Left
                if cur_piece.n % Jigsaw.width != 0:
                    left_piece = self.pieces[cur_piece.n - 1]
                    if left_piece.comp and dist(cur_piece.rect.midleft, left_piece.rect.midright) <= Jigsaw.EPS_H:
                        cur_piece.set_comp()
            self.pressed = -1
        else:
            if self.pressed != -1:
                self.pieces[self.pressed].rect.move_ip(event.rel)

    @staticmethod
    def check_victory():
        return Piece.comp_count == Jigsaw.width * Jigsaw.height


class Piece:
    width = None
    height = None

    comp_count = 0

    def __init__(self, n, image, offset):
        self.n = n

        self.orig_image = image.copy()
        self.surf = image
        self.rect = self.surf.get_rect(topleft=offset)
        self.make_shadow()

        self.comp = False

    def set_comp(self):
        if not self.comp:
            self.comp = True

            self.rect.topleft = (BORDER_SIZE + (self.n % Jigsaw.width) * Piece.width,
                                 BORDER_SIZE + (self.n // Jigsaw.width) * Piece.height)

            self.remove_shadow()

            Piece.comp_count += 1

            if Piece.comp_count > 4:
                pygame.mixer.music.play()

    def make_shadow(self):
        filler = pygame.Surface((Piece.width, Piece.height), flags=pygame.SRCALPHA)
        filler.fill(SHADOW_COLOR)
        self.surf.blit(filler, (0, 0))

    def remove_shadow(self):
        self.surf = self.orig_image

    def draw(self, screen):
        screen.blit(self.surf, self.rect.topleft)
