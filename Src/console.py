import pygame
import defs

class Console:
    def __init__(self):
        
        # Lấy thông tin màn hình
        display_info = pygame.display.Info()
        #screen_width = display_info.current_w
        screen_height = display_info.current_h
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
    
    def reSize_Smaller_Image(self, path):
        image = pygame.image.load(path).convert_alpha()
        width = int(image.get_width() * self.ratio_x * 0.75)
        height = int(image.get_height() * self.ratio_y * 0.75)
        image = pygame.transform.scale(image, (width, height))
        return image
    
    def reSize_Bigger_Image(self, path):
        image = pygame.image.load(path).convert_alpha()
        width = int(image.get_width() * self.ratio_x * 1.25)
        height = int(image.get_height() * self.ratio_y * 1.25)
        image = pygame.transform.scale(image, (width, height))
        return image
    
    def convertMatrix(self):
        defs.SQUARE_SIZE_DEFAULT = int(defs.SQUARE_SIZE_DEFAULT * self.ratio_cordinate)
        for i in range(6):
            for j in range(6):
                defs.MATRIX[i][j] = self.convertCoordinate((defs.MATRIX[i][j])[0], (defs.MATRIX[i][j])[1])            