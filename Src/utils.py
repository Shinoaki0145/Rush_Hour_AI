import pygame
import car
from manage_car import *
from defs import *

class GameUtils:
    def __init__(self, console):
        self.console = console
        self.selected_algorithm = None
        self.current_level = 1
        self.game_completed = False
        self.audio_muted = False  # Trạng thái âm thanh

        # đường dẫn đến các file âm thanh
        pygame.mixer.init()
        self.bg_music_path = AUDIO_PATH + "bg_music.mp3"
        self.win_music_path = AUDIO_PATH + "win_music.wav"
        self.fail_music_path = AUDIO_PATH + "fail_music.wav"

        pygame.mixer.music.load(self.bg_music_path)
        pygame.mixer.music.play(-1)  # Phát lặp vô hạn
    
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
            self.selected_algorithm = None
            return True
        elif action == "reset":
            return False
    
    def handle_lose_popup_action(self, action, game_popup):
        """
        Xử lý action từ lose popup - thiết kế tương tự handle_win_popup_action
        """
        game_popup.hide()
        self.game_completed = False
        
        if action == "reset":
            # Reset lại level hiện tại và reset thuật toán
            self.selected_algorithm = None  # Reset thuật toán
            return True  # Trả về True để báo hiệu cần reload map
        elif action == "exit":
            # Thoát game
            self.exit_game()
        return False
    
    def handle_final_win_1_popup_action(self, action, manage_car, game_popup):
        """
        Xử lý action từ final win 1 popup
        """
        if action == "next_popup":
            # Chuyển sang final_win_2 popup
            game_popup.show_final_win_2_message()
        elif action == "exit":
            # Thoát game
            self.exit_game()
        return manage_car

    def handle_final_win_2_popup_action(self, action, manage_car, game_popup, load_map_func):
        """
        Xử lý action từ final win 2 popup (code cũ)
        """
        if action.startswith("level_"):
            level = int(action.replace("level_", ""))
            map_name = f"map{level}"
            manage_car = load_map_func(map_name)
            self.current_level = level
            self.selected_algorithm = None
            game_popup.hide()
            self.game_completed = False
        elif action == "exit":
            self.exit_game()
        return manage_car

    def get_selected_algorithm(self):
        """Lấy algorithm hiện tại được chọn"""
        return self.selected_algorithm
    
    def has_selected_algorithm(self):
        """Kiểm tra xem đã chọn thuật toán chưa"""
        return self.selected_algorithm is not None
    
    def get_current_level(self):
        """Lấy level hiện tại"""
        return self.current_level
    
    def set_game_completed(self, completed=True):
        """Set trạng thái game completed"""
        self.game_completed = completed
    
    def is_game_completed(self):
        """Kiểm tra xem game đã hoàn thành chưa"""
        return self.game_completed
        
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
    
    # Xử lý âm thanh
    def play_win_music(self):
        pygame.mixer.music.load(self.win_music_path)
        pygame.mixer.music.play()

    def play_fail_music(self):
        pygame.mixer.music.load(self.fail_music_path)
        pygame.mixer.music.play()

    def play_bg_music(self):
        pygame.mixer.music.load(self.bg_music_path)
        pygame.mixer.music.play(-1)

    def toggle_mute(self):
        """Bật/tắt âm thanh"""
        self.audio_muted = not self.audio_muted
        if self.audio_muted:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(1)
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

    def check_lose_condition(self, path=None, algorithm_completed=False):
        if algorithm_completed and (path is None or len(path) == 0):
            return True
        
        return False
    
    def check_final_win_condition(self, manage_car):
        """
        Kiểm tra điều kiện final win (hoàn thành level 12)
        """
        if self.current_level == 12 and self.check_win_condition(manage_car):
            return True
        return False