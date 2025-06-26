import pygame
import car
from manage_car import *
from defs import *

class GameUtils:
    def __init__(self, console):
        self.console = console
    
    def check_button_click(self, mouse_pos, button_manager):
        """
        Check xem chuột có click vào button nào không
        Trả về tên button nếu có click, None nếu không
        """
        for button_name, button_data in button_manager.buttons.items():
            if button_data["rect"].collidepoint(mouse_pos):
                return button_name
        return None
    
    def handle_button_action(self, button_name, game_objects):
        """
        Xử lý action của button dựa trên tên button
        game_objects: dict chứa các object cần thiết của game
        """
        if button_name == "reset":
            return self.reset_game(game_objects)
        elif button_name == "exit":
            return self.exit_game()
        elif button_name == "stop":
            return self.pause_game(game_objects)
        elif button_name == "mute":
            return self.toggle_mute()
        elif button_name == "info":
            return self.show_info()
        return game_objects  # Trả về game_objects không thay đổi nếu không có action
    
    def reset_game(self, game_objects):
        """Reset game về trạng thái ban đầu"""
        # Tạo lại main_car
        main_car = car.MainCar(0, 2, self.console.reSize_Image(MAIN_CAR_PATH))
        car_1 = car.Car("car_1", 4, 0, self.console.reSize_Image(CAR_1), False, "down")
        
        # Tạo lại manage_car
        manage_car = ManageCar()
        manage_car.add_car(main_car)
        manage_car.add_car(car_1)
        
        # Cập nhật game_objects
        game_objects.update({
            "main_car": main_car,
            "car_1": car_1,
            "manage_car": manage_car
        })
        
        return game_objects
    
    def exit_game(self):
        """Thoát game"""
        pygame.quit()
        exit()
    
    def pause_game(self, game_objects):
        """Dừng tất cả cars"""
        if "manage_car" in game_objects:
            game_objects["manage_car"].pause_all_cars()
        return game_objects
    
    def toggle_mute(self):
        """Bật/tắt âm thanh"""
        self.console.toggle_audio()
        return True
    
    def show_info(self):
        """Hiển thị thông tin game"""
        self.console.show_info()
        return True
    
    def handle_keyboard_input(self, key, game_objects):
        """
        Xử lý input từ bàn phím
        """
        if "manage_car" in game_objects:
            if key == pygame.K_RIGHT:
                game_objects["manage_car"].move_car("main_car", "right")
            elif key == pygame.K_LEFT:
                game_objects["manage_car"].move_car("main_car", "left")
        return game_objects