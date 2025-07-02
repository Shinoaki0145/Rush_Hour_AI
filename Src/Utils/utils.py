import pygame
from Cars import *
from defs import *

class GameUtils:
    def __init__(self, console):
        self.console = console
        self.selected_algorithm = None
        self.current_level = 0
        self.game_completed = False
        self.audio_muted = False
        self.game_pause = False

        pygame.mixer.init()
        self.bg_music_path = AUDIO_PATH + "bg_music.wav"
        self.win_music_path = AUDIO_PATH + "win_music.wav"
        self.fail_music_path = AUDIO_PATH + "fail_music.wav"

        self.play_bg_music()
    
    def check_button_click(self, mouse_pos, button_manager):
        for button_name, button_data in button_manager.__dict__.items():
            if button_name in ['info', 'mute', 'pause', 'reset', 'play', 'exit']:
                if button_data.button["rect"].collidepoint(mouse_pos):
                    return button_data.name
        return None
    
    def handle_button_action(self, button_name, car_manager, game_popup=None):
        if button_name == "reset":
            return self.reset_game(car_manager)
        elif button_name == "exit":
            return self.exit_game()
        elif button_name == "play":
            return self.play_game(game_popup)
        elif button_name == "pause":
            return self.pause_game()
        elif button_name == "mute":
            return self.toggle_mute()
        elif button_name == "info":
            return self.show_info(game_popup)
        return car_manager  # Trả về car_manager không thay đổi nếu không có action

    def handle_button_action_menu(self, button_game, game_popup = None):
        if button_game == "play":
            return self.play_game(game_popup)
        elif button_game == "mute":
            return self.toggle_mute()
        elif button_game == "info":
            return self.show_info_menu(game_popup)
        
    def handle_algorithm_selection(self, algorithm):
        self.selected_algorithm = algorithm
        self.game_completed = False

    def reset_game(self, car_manager):
        return car_manager
    
    def handle_win_popup_action(self, action, game_popup):
        game_popup.hide()
        self.game_completed = False
        if action == "next_level":
            self.current_level += 1
            self.selected_algorithm = None
            return True
        elif action == "reset":
            return False
    
    def handle_lose_popup_action(self, action, game_popup):
        game_popup.hide()
        self.game_completed = False
        
        if action == "reset":
            self.selected_algorithm = None
            return True
        elif action == "exit":
            self.exit_game()
        return False
    
    def handle_final_win_popup_action(self, action, car_manager, game_popup):
        if action == "next_popup":
            game_popup.hide()
            self.current_level = 0
            self.selected_algorithm = None
            self.game_completed = False
            return "return_to_menu"
        elif action == "exit":
            self.exit_game()
        return car_manager

    def handle_choose_level_popup_action(self, action, car_manager, game_popup, console, load_map_func):
        if action.startswith("level_"):
            level = int(action.replace("level_", ""))
            map_name = f"map{level}"
            car_manager = load_map_func(console, map_name)
            self.current_level = level
            self.selected_algorithm = None
            game_popup.hide()
            self.game_completed = False
        elif action == "exit":
            self.exit_game()
        return car_manager
    
    def handle_info_in_game_popup_action(self, action, game_popup):
        if action == "back_button":
            game_popup.hide()

    def handle_info_in_game_popup_action(self, action, game_popup):
        if action == "back_button":
            game_popup.hide()

    def get_selected_algorithm(self):
        return self.selected_algorithm
    
    def has_selected_algorithm(self):
        return self.selected_algorithm is not None
    
    def get_current_level(self):
        return self.current_level
    
    def set_game_completed(self, completed=True):
        self.game_completed = completed
    
    def is_game_completed(self):
        return self.game_completed
        
    def exit_game(self):
        pygame.quit()
        exit()
            
    def play_game(self, game_popup=None):
        if game_popup:
            # game_popup.show_algorithm_selection()  # CẬP NHẬT: Chỉ show popup, không chờ return
            # game_popup.update(True, "algorithm")
            game_popup.show_algorithm_selection()
    
    def pause_game(self):
        """Dừng tất cả cars"""
        self.game_pause = not self.game_pause
    
    # Xử lý âm thanh
    def play_win_music(self):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.win_music_path))

    def play_fail_music(self):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.fail_music_path))

    def play_bg_music(self):
        pygame.mixer.music.load(self.bg_music_path)
        pygame.mixer.music.play(-1)

    def toggle_mute(self):
        self.audio_muted = not self.audio_muted
        if self.audio_muted:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(1)
        return True
    
    def show_info(self, game_popup=None):
        if game_popup:
            game_popup.show_info_in_game()

    def show_info_menu(self, game_popup=None):
        if game_popup:
            game_popup.show_info_menu()
    
    def handle_keyboard_input(self, key, car_manager):
        if key == pygame.K_RIGHT:
            car_manager.move_car("main_car", "right")
        elif key == pygame.K_LEFT:
            car_manager.move_car("main_car", "left")
        return car_manager
    
    def check_win_condition(self, car_manager):
        target_car = car_manager.cars["target_car"]
        if target_car and target_car.is_at_exit():
            return True
        return False

    def check_lose_condition(self, path=None, algorithm_completed=False):
        if algorithm_completed and (path is None or len(path) == 0):
            return True
        return False
    
    def check_final_win_condition(self, car_manager):
        if self.current_level == 12 and self.check_win_condition(car_manager):
            return True
        return False