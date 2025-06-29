import pygame
import car
from manage_car import *
from defs import *

class GameUtils:
    def __init__(self, console):
        self.console = console
        self.selected_algorithm = "A STAR"  # Default algorithm
        self.current_level = 1
        self.game_completed = False
    
    def check_button_click(self, mouse_pos, button_manager):
        """
        Check xem chuột có click vào button nào không
        Trả về tên button nếu có click, None nếu không
        """
        for button_name, button_data in button_manager.buttons.items():
            if button_data["rect"].collidepoint(mouse_pos):
                return button_name
        return None
    
    def handle_button_action(self, button_name, manage_car, game_popup=None):
        """
        Xử lý action của button dựa trên tên button
        game_popup: GamePopup object
        """
        if button_name == "reset":
            return self.reset_game(manage_car)
        elif button_name == "exit":
            return self.exit_game()
        elif button_name == "play":
            return self.play_game(game_popup)
        elif button_name == "stop":
            return self.pause_game(manage_car)
        elif button_name == "mute":
            return self.toggle_mute()
        elif button_name == "info":
            return self.show_info()
        return manage_car  # Trả về manage_car không thay đổi nếu không có action
    
    def handle_algorithm_selection(self, algorithm):
        """
        Xử lý khi người chơi chọn algorithm
        """
        self.selected_algorithm = algorithm
        print(f"GameUtils: Selected algorithm changed to: {algorithm}")
        
        # Reset game completed flag
        self.game_completed = False

    def reset_game(self, manage_car):
        return manage_car
    
    def handle_win_popup_action(self, action, game_popup):
        """
        Xử lý action từ win popup
        """
        game_popup.hide()
        self.game_completed = False
        if action == "next_level":
            # Chuyển sang level tiếp theo
            self.current_level += 1
            return True
        elif action == "reset":
            return False
    def get_selected_algorithm(self):
        """Lấy algorithm hiện tại được chọn"""
        return self.selected_algorithm
    
    def get_current_level(self):
        """Lấy level hiện tại"""
        return self.current_level
    
    def set_game_completed(self, completed=True):
        """Set trạng thái game completed"""
        self.game_completed = completed
    
    def is_game_completed(self):
        """Kiểm tra xem game đã hoàn thành chưa"""
        return self.game_completed
    
    #def reset_game(self, game_objects):
        
    def exit_game(self):
        """Thoát game"""
        pygame.quit()
        exit()
            
    def play_game(self, game_popup=None):
        """Hiển thị popup để chọn algorithm"""
        if game_popup:
            game_popup.show_algorithm_selection()  # CẬP NHẬT: Chỉ show popup, không chờ return
    
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
    
    def check_win_condition(self, manage_car):
        """
        Kiểm tra điều kiện thắng game
        """
        target_car = manage_car.cars["target_car"]
        if target_car and target_car.is_at_exit():
            return True
        return False
