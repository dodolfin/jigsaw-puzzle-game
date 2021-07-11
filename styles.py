from parameters import *


class DefaultStyle:
    background_color = WHITE
    color = BLACK

    border_color = (128, 128, 128)
    border_width = 1

    padding = 5

    font_name = 'Open Sans'
    font_size = 20


class PressedStyle(DefaultStyle):
    background_color = BLACK
    color = WHITE


class HoveredStyle(DefaultStyle):
    background_color = (210, 210, 210)
    color = BLACK
