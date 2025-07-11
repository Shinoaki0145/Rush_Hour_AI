import pygame
import defs

class SimpleCar:
    def __init__(self, name, length, coord, vertical):
        self.name = name
        self.length = length
        self.coord = coord  # (y, x)
        self.vertical = vertical
        self.axis = 0 if self.vertical else 1  # 0 là trục y (dọc), 1 là trục x (ngang)
        
class Car:
    def __init__(self, name, x, y, image, is_horizontal, direc):
        self.name = name
        self.x = x
        self.y = y
        self.offset_x, self.offset_y = defs.MATRIX[y][x]
        self.image = image 
        self.length_grid = round(self.image.get_width() / defs.SQUARE_SIZE_DEFAULT)
        self.is_horizontal = is_horizontal
        if(is_horizontal):
            if direc == "left":
                self.image = pygame.transform.rotate(image, 180)
        else:
            if direc == "up":
                self.image = pygame.transform.rotate(image, 90)
            elif direc == "down":
                self.image = pygame.transform.rotate(image, -90)

    def update(self):
        x_coor, y_coor = defs.MATRIX[self.y][self.x]
        if self.offset_x < x_coor:
            self.offset_x += defs.MOVE_SPEED
            if self.offset_x > x_coor:
                self.offset_x = x_coor
        elif self.offset_x > x_coor:
            self.offset_x -= defs.MOVE_SPEED
            if self.offset_x < x_coor:
                self.offset_x = x_coor

        if self.offset_y < y_coor:
            self.offset_y += defs.MOVE_SPEED
            if self.offset_y > y_coor:
                self.offset_y = y_coor
        elif self.offset_y > y_coor:
            self.offset_y -= defs.MOVE_SPEED
            if self.offset_y < y_coor:
                self.offset_y = y_coor
        return self.offset_x != x_coor or self.offset_y != y_coor
    
    def draw(self, surface):
        surface.blit(self.image, (self.offset_x, self.offset_y))


class MainCar(Car):
    def __init__(self, x, y, image):
        super().__init__("target_car", x, y, image, is_horizontal = True, direc = "right")

    def is_at_exit(self):
        return self.x == 4
    
    def update(self):
        if self.is_at_exit():
            self.offset_x += defs.EXIT_MOVE_SPEED
        else:
            super().update()
