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
    
    def handle_button_action(self, button_name, manage_car):
        if button_name == "reset":
            return self.reset_game(manage_car)
        elif button_name == "exit":
            return self.exit_game()
        elif button_name == "play":
            return self.pause_game(manage_car)  # Giả sử play cũng dừng game
        elif button_name == "stop":
            return self.pause_game(manage_car)
        elif button_name == "mute":
            return self.toggle_mute()
        elif button_name == "info":
            return self.show_info()
        return manage_car  # Trả về manage_car không thay đổi nếu không có action
    
    def reset_game(self, manage_car):
        
        return manage_car
    
    def exit_game(self):
        """Thoát game"""
        pygame.quit()
        exit()
        
    def play_game(self, manage_car):
        """Bắt đầu hoặc tiếp tục game"""
        manage_car.start_all_cars()
        return manage_car
    
    def pause_game(self, manage_car):
        """Dừng tất cả cars"""
        manage_car.pause_all_cars()
        return manage_car
    
    def toggle_mute(self):
        """Bật/tắt âm thanh"""
        self.console.toggle_audio()
        return True
    
    def show_info(self):
        """Hiển thị thông tin game"""
        self.console.show_info()
        return True
    
    def handle_keyboard_input(self, key, manage_car):
        """
        Xử lý input từ bàn phím
        """
        if key == pygame.K_RIGHT:
            manage_car.move_car("main_car", "right")
        elif key == pygame.K_LEFT:
            manage_car.move_car("main_car", "left")
        return manage_car