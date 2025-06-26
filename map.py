import pygame

class Board:
    def __init__(self, image, title_size, offset_x, offset_y):
        self.image = image
        self.title_size = title_size
        self.offset_x = offset_x
        self.offset_y = offset_y

    def grid_to_pixel(self, row, col):
        x = self.offset_x + col * self.title_size
        y = self.offset_y + row * self.title_size
        return x, y
    
    def pixel_to_grid(self, x, y):
        col = (x - self.offset_x) // self.title_size
        row = (y - self.offset_y) // self.title_size
        return row, col 