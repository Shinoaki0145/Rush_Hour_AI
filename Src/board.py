import pygame

class Board:
    def __init__(self, image, title_size, offset_x, offset_y):
        self.image = image
        self.title_size = title_size
        self.offset_x = offset_x
        self.offset_y = offset_y