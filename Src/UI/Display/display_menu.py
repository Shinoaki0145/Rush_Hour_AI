from Cars import *

class DisplayMenu:
    def __init__(self, console, button_menu, board, flag):
        self.console = console
        self.button_menu = button_menu
        self.bg_img = board
        self.flag = flag
        self.setup_menu()
    
    def setup_menu(self):
        self.manage_car = ManageCar()
        car1 = Car("car_target", 0, 2, self.console.reSize_Image("Asset/Car/car_target.png"), True, "right")
        car2 = Car("car_1", 3, 3, self.console.reSize_Image("Asset/Car/car_0.png"), False, "down")
        car3 = Car("car_2", 4, 0, self.console.reSize_Image("Asset/Car/truck_1.png"), False, "down")
        car4 = Car("car_3", 4, 4, self.console.reSize_Image("Asset/Car/car_2.png"), True, "right")
        self.manage_car.add_car(car1)
        self.manage_car.add_car(car2)
        self.manage_car.add_car(car3)
        self.manage_car.add_car(car4)
    
    def draw_menu(self, surface):
        surface.blit(self.bg_img, (0, 0))
        self.manage_car.draw_all(surface)
        self.button_menu.draw_all(surface)