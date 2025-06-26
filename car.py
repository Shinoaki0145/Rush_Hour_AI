import pygame
import defs

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

    def get_next_positions(self, direction):
        if self.is_horizontal:
            if direction == "right":
                return (self.x + self.length_grid, self.y)
            elif direction == "left":
                return (self.x - 1, self.y)
        else:
            if direction == "down":
                return (self.x, self.y + self.length_grid)
            elif direction == "up":
                return (self.x, self.y - 1)
        return ()
    
    def move(self, direction):
        if self.is_horizontal:
            if direction == "right":
                defs.VALID_MATRIX[self.y][self.x] = 0
                defs.VALID_MATRIX[self.y][self.x + self.length_grid] = 1
                self.x += 1

            elif direction == "left":
                defs.VALID_MATRIX[self.y][self.x + self.length_grid - 1] = 0
                defs.VALID_MATRIX[self.y][self.x - 1] = 1
                self.x -= 1

        else:
            if direction == "down":
                defs.VALID_MATRIX[self.y][self.x] = 0
                defs.VALID_MATRIX[self.y + self.length_grid][self.x] = 1
                self.y += 1

            elif direction == "up":
                defs.VALID_MATRIX[self.y + self.length_grid - 1][self.x] = 0
                defs.VALID_MATRIX[self.y - 1][self.x] = 1
                self.y -= 1

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

    def draw(self, surface):
        surface.blit(self.image, (self.offset_x, self.offset_y))


class MainCar(Car):
    def __init__(self, x, y, image):
        super().__init__("main_car", x, y, image, is_horizontal = True, direc = "right")

    def is_at_exit(self):
        return self.x + self.length_grid - 1 == 5
