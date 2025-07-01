import pygame
import Cars.car
from defs import *

class ManageCar:
    def __init__(self):
        self.row = 6
        self.col = 6
        self.cars = {}

    def add_car(self, car):
        if car.is_horizontal:
            if car.length_grid + car.x - 1 > self.col:
                return False
            for i in range(car.length_grid):
                if VALID_MATRIX[car.y][car.x + i]:
                    return False
        else:
            if car.length_grid + car.y - 1 > self.col:
                return False
            for i in range(car.length_grid):
                if VALID_MATRIX[car.y + i][car.x]:
                    return False
        
        if car.is_horizontal:
            for i in range(car.length_grid):
                VALID_MATRIX[car.y][car.x + i] = 1
        else:
            for i in range(car.length_grid):
                VALID_MATRIX[car.y + i][car.x] = 1

        self.cars[car.name] = car
        # print(self.cars)
        return True
    
    def can_move(self, car_name, direction):
        car = self.cars.get(car_name)
        if not car:
            return False
        next_cells = car.get_next_positions(direction)
        x, y = next_cells
        print(x, y)
        if not (0 <= x < (self.col) and 0 <= y < (self.row)):
            return False    
        if not VALID_MATRIX[y][x]:
            return True
        else:
            return False
        
    def move_car(self, car_name, direction):
        car = self.cars.get(car_name)
        if self.can_move(car_name, direction):
            car.move(direction)
            print(VALID_MATRIX)
        else:
            print("Cannot move !!!")

    def update_car(self):
        updated = False
        for car in self.cars.values():
            if car.update():
                updated = True
        return updated

    def draw_all(self, surface):
        for car in self.cars.values():
            car.draw(surface)
