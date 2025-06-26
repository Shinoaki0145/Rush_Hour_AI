import pygame
import ctypes
import defs

class Console:
    def __init__(self):
        user32 = ctypes.windll.user32
        screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        screen_height = screen_height - defs.HEADER_BAR

        self.screen_size = screen_height
        self.ratio_y = (screen_height) / defs.MAP_SIZE[1]
        self.ratio_x = (screen_height) / defs.MAP_SIZE[0]
        self.ratio_cordinate = (screen_height) / defs.HEIGHT_DEFAULT
    
    def convertCoordinate(self, x, y):
        x = int(x * self.ratio_cordinate)
        y = int(y * self.ratio_cordinate)
        return x, y

    def reSize_Image(self, path):
        image = pygame.image.load(path).convert_alpha()
        width = int(image.get_width() * self.ratio_x)
        height = int(image.get_height() * self.ratio_y)
        image = pygame.transform.scale(image, (width, height))
        return image
    
    def convertMatrix(self):
        defs.SQUARE_SIZE_DEFAULT = int(defs.SQUARE_SIZE_DEFAULT * self.ratio_cordinate)
        for i in range(6):
            for j in range(6):
                defs.MATRIX[i][j] = self.convertCoordinate((defs.MATRIX[i][j])[0], (defs.MATRIX[i][j])[1])