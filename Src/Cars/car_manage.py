import pygame
import Cars.car
from defs import *

class CarManager:
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
        return True

    def update_car(self):
        updated = False
        for car in self.cars.values():
            if car.update():
                updated = True
        return updated

    def draw_all(self, surface):
        for car in self.cars.values():
            car.draw(surface)
