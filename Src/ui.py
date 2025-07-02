import pygame
from defs import *
from manage_car import *
from car import *

class GamePopup:
    def __init__(self, console):
        self.console = console
        self.visible = False
        self.popup_type = None
        self.buttons = {}
        self.setup_popup()
        
        self.level = 0
        self.moves = 0
        self.cost = 0
        self.algorithm = ""
        
        self.win_button_images = {
            "reset_level": self.console.reSize_Image(BUTTON_PATH + "but_reset.png"),
            "next_level": self.console.reSize_Image(BUTTON_PATH + "but_play.png")
        }
        
        self.lose_button_images = {
            "reset_level": self.console.reSize_Image(BUTTON_PATH + "but_reset.png"),
            "exit_level": self.console.reSize_Image(BUTTON_PATH + "but_exit.png")
        }
        
        self.final_win_button_images = {
            "exit_level": self.console.reSize_Image(BUTTON_PATH + "but_exit.png"),
            "next_popup": self.console.reSize_Image(BUTTON_PATH + "but_play.png")  # Dùng play button cho "next"
        }
        self.choose_level_button_images = {
            "level_button": self.console.reSize_Image(BUTTON_PATH + "level_unlock.png"),
        }
    
        self.info_in_game = {
            "play_button": self.console.reSize_Smaller_Image(BUTTON_PATH + "but_play.png"),
            "pause_button": self.console.reSize_Smaller_Image(BUTTON_PATH + "but_pause.png"),
            "exit_button": self.console.reSize_Smaller_Image(BUTTON_PATH + "but_exit.png"),
            "back_button": self.console.reSize_Smaller_Image(BUTTON_PATH + "but_back.png")
        }

        self.info_menu = {
            "back_button": self.console.reSize_Smaller_Image(BUTTON_PATH + "but_back.png")
        }
        
    def setup_popup(self):
        """Setup popup background"""
        self.popup_bg = self.console.reSize_Image(DISPLAY_PATH + "msg_display.png")
        
        # Tính toán vị trí giữa màn hình
        self.popup_pos = (
            (self.console.screen_size - self.popup_bg.get_width()) // 2,
            (self.console.screen_size - self.popup_bg.get_height()) // 2
        )
    
    def show_algorithm_selection(self):
        self.popup_type = "algorithm"
        self.visible = True
        self.setup_algorithm_buttons()

    def show_win_message(self, level, moves, cost, algorithm="DFS"):
        self.popup_type = "win"
        self.visible = True
        self.level = level
        self.moves = moves
        self.cost = cost
        self.algorithm = algorithm
        self.setup_win_buttons()
        
    def show_lose_message(self, level, algorithm="DFS"):
        self.popup_type = "lose"
        self.visible = True
        self.level = level
        self.algorithm = algorithm
        self.setup_lose_buttons()
        
    def show_final_win_message(self, level, moves, cost, algorithm="DFS"):
        self.popup_type = "final_win"
        self.visible = True
        self.level = level
        self.moves = moves
        self.cost = cost
        self.algorithm = algorithm
        self.setup_final_win_buttons()
    
    def show_choose_level_message(self):
        self.popup_type = "choose_level"
        self.visible = True
        self.setup_choose_level_buttons()

    def show_info_in_game(self):
        self.popup_type = "info_buttons"
        self.visible = True
        self.selected_option = None
        self.setup_info_in_game()

    def show_info_menu(self):
        self.popup_type = "info_menu"
        self.visible = True
        self.selected_option = None
        self.setup_info_menu()

    def setup_algorithm_buttons(self):
        self.buttons = {}

        button_image = self.console.reSize_Image(BUTTON_PATH + "but_start.png")
        
        algorithms = ["BFS", "DFS", "A STAR", "UCS"]
        button_width = button_image.get_width()
        button_height = button_image.get_height()
        
        # (2x2 grid)
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2
        
        spacing_x = 20
        spacing_y = 20
        
        positions = [
            (popup_center_x - button_width - spacing_x//2, popup_center_y - button_height - spacing_y//2),  # BFS
            (popup_center_x + spacing_x//2, popup_center_y - button_height - spacing_y//2),  # DFS
            (popup_center_x - button_width - spacing_x//2, popup_center_y + spacing_y//2),  # A STAR
            (popup_center_x + spacing_x//2, popup_center_y + spacing_y//2)   # UCS
        ]
        
        for i, algorithm in enumerate(algorithms):
            self.buttons[algorithm] = {
                "image": button_image,
                "pos": positions[i],
                "rect": pygame.Rect(positions[i][0], positions[i][1], button_width, button_height),
                "text": algorithm
            }
    
    def setup_win_buttons(self):
        self.buttons = {}

        reset_button_image = self.win_button_images["reset_level"]
        next_button_image = self.win_button_images["next_level"]
        
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2 + 40
        
        spacing_x = 30
        
        reset_button_width = reset_button_image.get_width()
        next_button_width = next_button_image.get_width()
        
        reset_pos = (popup_center_x - reset_button_width - spacing_x//2, popup_center_y)
        next_pos = (popup_center_x + spacing_x//2, popup_center_y)
        
        self.buttons["reset"] = {
            "image": reset_button_image,
            "pos": reset_pos,
            "rect": pygame.Rect(reset_pos[0], reset_pos[1], reset_button_width, reset_button_image.get_height()),
        }
        
        self.buttons["next_level"] = {
            "image": next_button_image,
            "pos": next_pos,
            "rect": pygame.Rect(next_pos[0], next_pos[1], next_button_width, next_button_image.get_height()),
        }

    def setup_lose_buttons(self):
        self.buttons = {}

        reset_button_image = self.lose_button_images["reset_level"]
        exit_button_image = self.lose_button_images["exit_level"]

        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2 + 40
        
        spacing_x = 30
        
        reset_button_width = reset_button_image.get_width()
        exit_button_width = exit_button_image.get_width()
        
        reset_pos = (popup_center_x - reset_button_width - spacing_x//2, popup_center_y)
        exit_pos = (popup_center_x + spacing_x//2, popup_center_y)
        
        self.buttons["reset"] = {
            "image": reset_button_image,
            "pos": reset_pos,
            "rect": pygame.Rect(reset_pos[0], reset_pos[1], reset_button_width, reset_button_image.get_height()),
        }

        self.buttons["exit"] = {
            "image": exit_button_image,
            "pos": exit_pos,
            "rect": pygame.Rect(exit_pos[0], exit_pos[1], exit_button_width, exit_button_image.get_height()),
        }
        
    def setup_final_win_buttons(self):
        self.buttons = {}

        exit_button_image = self.final_win_button_images["exit_level"]
        next_button_image = self.final_win_button_images["next_popup"]
        
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2 + 40
        
        spacing_x = 30
        
        exit_button_width = exit_button_image.get_width()
        next_button_width = next_button_image.get_width()
        
        exit_pos = (popup_center_x - exit_button_width - spacing_x//2, popup_center_y)
        next_pos = (popup_center_x + spacing_x//2, popup_center_y)
        
        self.buttons["exit"] = {
            "image": exit_button_image,
            "pos": exit_pos,
            "rect": pygame.Rect(exit_pos[0], exit_pos[1], exit_button_width, exit_button_image.get_height()),
        }
        
        self.buttons["next_popup"] = {
            "image": next_button_image,
            "pos": next_pos,
            "rect": pygame.Rect(next_pos[0], next_pos[1], next_button_width, next_button_image.get_height()),
        }
        
    def setup_choose_level_buttons(self):
        self.buttons = {}

        level_button_image = self.choose_level_button_images["level_button"]
        button_width = level_button_image.get_width()
        button_height = level_button_image.get_height()

        # (3 rows × 4 columns)
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2
        spacing_x = 15
        spacing_y = 15

        # grid 3×4
        total_width = 4 * button_width + 3 * spacing_x
        total_height = 3 * button_height + 2 * spacing_y
        
        start_x = popup_center_x - total_width // 2
        start_y = popup_center_y - total_height // 2

        for i in range(12):
            row = i // 4
            col = i % 4
            
            level_pos = (
                start_x + col * (button_width + spacing_x),
                start_y + row * (button_height + spacing_y)
            )
            
            level_name = str(i + 1)
            self.buttons[f"level_{level_name}"] = {
                "image": level_button_image,
                "pos": level_pos,
                "rect": pygame.Rect(level_pos[0], level_pos[1], button_width, button_height),
                "text": level_name
            }
    def setup_info_in_game(self):
        self.buttons = {}

        play_button_image = self.info_in_game["play_button"]
        pause_button_image = self.info_in_game["pause_button"]
        exit_button_image = self.info_in_game["exit_button"]
        back_button_image = self.info_in_game["back_button"]

        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2

        play_button_width = play_button_image.get_width()

        spacing_x = 100
        spacing_y = 20
        spacing_line = 70

        play_pos = (popup_center_x - play_button_width - spacing_x, popup_center_y - play_button_width - spacing_y)

        self.buttons["play_button"] = {
            "image": play_button_image,
            "pos": play_pos,
            "rect": pygame.Rect(play_pos[0], play_pos[1], play_button_width, play_button_image.get_height()),
        }

        pause_pos = (popup_center_x - play_button_width - spacing_x, popup_center_y - play_button_width - spacing_y + spacing_line)

        self.buttons["pause_button"] = {
            "image": pause_button_image,
            "pos": pause_pos,
            "rect": pygame.Rect(pause_pos[0], pause_pos[1], play_button_width, play_button_image.get_height()),
        }

        exit_pos = (popup_center_x - play_button_width - spacing_x, popup_center_y - play_button_width - spacing_y + 2 * spacing_line)

        self.buttons["exit_button"] = {
            "image": exit_button_image,
            "pos": exit_pos,
            "rect": pygame.Rect(exit_pos[0], exit_pos[1], play_button_width, play_button_image.get_height()),
        }

        back_pos = (popup_center_x - play_button_width -  spacing_x + 300, popup_center_y - play_button_width - 110)

        self.buttons["back_button"] = {
            "image": back_button_image,
            "pos": back_pos,
            "rect": pygame.Rect(back_pos[0], back_pos[1], play_button_width, play_button_image.get_height()),
        }

    
    def setup_info_menu(self):
        self.buttons = {}
        back_button_image = self.info_in_game["back_button"]
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2
        back_button_width = back_button_image.get_width()
        back_pos = (popup_center_x - back_button_width -  100 + 300, popup_center_y - back_button_width - 110)

        self.buttons["back_button"] = {
            "image": back_button_image,
            "pos": back_pos,
            "rect": pygame.Rect(back_pos[0], back_pos[1], back_button_width, back_button_image.get_height()),
        }

    def hide(self):
        self.visible = False
        self.popup_type = None
    
    def draw(self, screen):
        if not self.visible:
            return
        
        # Vẽ popup background
        screen.blit(self.popup_bg, self.popup_pos)
        
        if self.popup_type == "algorithm":
            self.draw_algorithm_popup(screen)
        elif self.popup_type == "win":
            self.draw_win_popup(screen)
        elif self.popup_type == "lose":
            self.draw_lose_popup(screen)
        elif self.popup_type == "final_win":
            self.draw_final_win_popup(screen)
        elif self.popup_type == "choose_level":
            self.draw_choose_level_popup(screen)
        elif self.popup_type == "info_buttons":
            self.draw_info_in_game(screen)
        elif self.popup_type == "info_menu":
            self.draw_info_menu(screen)
    
    def draw_algorithm_popup(self, screen):
        title_x = self.popup_pos[0] + self.popup_bg.get_width() // 2 - 120
        title_y = self.popup_pos[1] + 50
        create_3d_text(screen, "CHOOSE ALGORITHM", 24, title_x, title_y)
        
        for algorithm, button_data in self.buttons.items():
            screen.blit(button_data["image"], button_data["pos"])
            
            text_x = button_data["pos"][0] + button_data["image"].get_width() // 2 - len(algorithm) * 6
            text_y = button_data["pos"][1] + button_data["image"].get_height() // 2 - 10
            create_3d_text(screen, algorithm, 16, text_x, text_y)
    
    def draw_win_popup(self, screen):
        congrat_text = f"CONGRATULATIONS!"
        info_text_1 = f"YOU WIN LEVEL {self.level}"
        info_text_2 = f"WITH {self.moves} MOVES AND COST {self.cost} UNITS"
        algorithm_text = f"BY USING ALGORITHM: {self.algorithm}"
        
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        
        title_x = popup_center_x - len(congrat_text) * 4 - 40
        title_y = self.popup_pos[1] + 30
        create_3d_text(screen, congrat_text, 20, title_x, title_y)
        
        info_x = popup_center_x - len(info_text_1) * 4 - 20
        info_y = self.popup_pos[1] + 80
        create_3d_text(screen, info_text_1, 16, info_x, info_y)
        
        info_x_2 = popup_center_x - len(info_text_2) * 4 - 20
        info_y_2 = self.popup_pos[1] + 100
        create_3d_text(screen, info_text_2, 16, info_x_2, info_y_2)

        algorithm_x = popup_center_x - len(algorithm_text) * 4
        algorithm_y = self.popup_pos[1] + 120
        create_3d_text(screen, algorithm_text, 16, algorithm_x, algorithm_y)
        
        for button_name, button_data in self.buttons.items():

            screen.blit(button_data["image"], button_data["pos"])
    
    def draw_lose_popup(self, screen):
        congrat_text = f"YOU LOST!"
        info_text = f"YOU FAILED LEVEL {self.level}"
        algorithm_text = f"BY USING ALGORITHM: {self.algorithm}"
        
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        
        title_x = popup_center_x - len(congrat_text) * 4 - 20
        title_y = self.popup_pos[1] + 50
        create_3d_text(screen, congrat_text, 20, title_x, title_y)
        
        info_x = popup_center_x - len(info_text) * 4 - 20
        info_y = self.popup_pos[1] + 100
        create_3d_text(screen, info_text, 16, info_x, info_y)
        
        algorithm_x = popup_center_x - len(algorithm_text) * 4
        algorithm_y = self.popup_pos[1] + 130
        create_3d_text(screen, algorithm_text, 16, algorithm_x, algorithm_y)
        
        for button_name, button_data in self.buttons.items():
            screen.blit(button_data["image"], button_data["pos"])
    
    def draw_final_win_popup(self, screen):
        congrat_text = f"FANTASTIC BABY!"
        info_text_1 = f"YOU FINAL WIN LEVEL {self.level}"
        info_text_2 = f"WITH {self.moves} MOVES AND COST {self.cost} UNITS"
        algorithm_text = f"BY USING ALGORITHM: {self.algorithm}"
        
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        
        title_x = popup_center_x - len(congrat_text) * 4 - 40
        title_y = self.popup_pos[1] + 30
        create_3d_text(screen, congrat_text, 20, title_x, title_y)
        
        info_x = popup_center_x - len(info_text_1) * 4 - 20
        info_y = self.popup_pos[1] + 80
        create_3d_text(screen, info_text_1, 16, info_x, info_y)
        
        info_x_2 = popup_center_x - len(info_text_2) * 4 - 20
        info_y_2 = self.popup_pos[1] + 100
        create_3d_text(screen, info_text_2, 16, info_x_2, info_y_2)

        algorithm_x = popup_center_x - len(algorithm_text) * 4
        algorithm_y = self.popup_pos[1] + 120
        create_3d_text(screen, algorithm_text, 16, algorithm_x, algorithm_y)
        
        for button_name, button_data in self.buttons.items():
            screen.blit(button_data["image"], button_data["pos"])
    
    def draw_choose_level_popup(self, screen):
        win_text = "Select a level to start playing"
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        win_text_x = popup_center_x - len(win_text) * 4 - 17
        win_text_y = self.popup_pos[1] + 20
        create_3d_text(screen, win_text, 20, win_text_x, win_text_y)
        
        for button_name, button_data in self.buttons.items():
            adjusted_pos = (button_data["pos"][0], button_data["pos"][1] + 20)
            screen.blit(button_data["image"], adjusted_pos)
            level_text = button_data["text"]
            text_x = adjusted_pos[0] + button_data["image"].get_width() // 2 - len(level_text) * 4
            text_y = adjusted_pos[1] + button_data["image"].get_height() // 2 - 15
            create_3d_text(screen, level_text, 20, text_x, text_y)
            
    def draw_info_in_game(self, screen):
        title_x = self.popup_pos[0] + self.popup_bg.get_width() // 2 - 135
        title_y = self.popup_pos[1] + 15
        create_3d_text(screen, "INFO BUTTON IN GAME", 24, title_x, title_y)

        create_3d_text(screen, "PRESS PLAY TO CHOOSE ALGORITHM", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 80)
        create_3d_text(screen, "PRESS PAUSE", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 140)
        create_3d_text(screen, "PRESS AGAIN TO CONTINUE", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 160)
        create_3d_text(screen, "PRESS EXIT TO OUT GAME", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 220)

        for button_name, button_data in self.buttons.items():
            screen.blit(button_data["image"], button_data["pos"])
    
    def draw_info_menu(self, screen):
        title_x = self.popup_pos[0] + self.popup_bg.get_width() // 2 - 110
        title_y = self.popup_pos[1] + 15
        create_3d_text(screen, "RUSH HOUR", 40, title_x, title_y)

        create_3d_text(screen, "GROUP 4", 25, title_x + 60, title_y + 50)
        create_3d_text(screen, "TRAN HOAI THIEN NHAN", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 120)
        create_3d_text(screen, "TTRAN TRI NHAN", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 160)
        create_3d_text(screen, "NNGUYEN AN NGHIEP", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 200)
        create_3d_text(screen, "CCAO TRAN BA DAT", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 240)

        for button_name, button_data in self.buttons.items():
            screen.blit(button_data["image"], button_data["pos"])

    def check_button_click(self, mouse_pos):
        if not self.visible:
            return None
        
        for button_name, button_data in self.buttons.items():
            if button_data["rect"].collidepoint(mouse_pos):        
                return button_name
        return None

class DisplayManager:
    def __init__(self, console):
        self.console = console
        self.displays = {}
        self.load_display_images()
        self.setup_display_positions()
    
    def load_display_images(self):
        self.display_images = {
            "algorithm": self.console.reSize_Image(DISPLAY_PATH + "algo_display.png"),
            "level": self.console.reSize_Image(DISPLAY_PATH + "level_display.png"),
            "moves": self.console.reSize_Image(DISPLAY_PATH + "moves_display.png"),
            "costs": self.console.reSize_Image(DISPLAY_PATH + "level_display.png")
        }
    
    def setup_display_positions(self):
        self.displays = {
            "algorithm": {
                "image": self.display_images["algorithm"],
                "pos": (self.console.screen_size // 2 - 85, 175),
                "text_pos": (self.console.screen_size // 2 - 55, 179),
                "text": "ALGORITHM :  "
            },
            "level": {
                "image": self.display_images["level"], 
                "pos": (205, 175),
                "text_pos": (222, 179),
                "text": "LEVEL :  0"
            },
            "moves": {
                "image": self.display_images["moves"],
                "pos": (self.console.screen_size - 300, 175),
                "text_pos": (self.console.screen_size - 286, 179),
                "text": "MOVES :  0"
            },
            "costs": {
                "image": self.display_images["costs"],
                "pos": (self.console.screen_size - 190, 175),
                "text_pos": (self.console.screen_size - 177, 179),
                "text": "COSTS :  0"
            }
        }
    
    def draw_display(self, screen, display_name):
        if display_name in self.displays:
            display = self.displays[display_name]
            screen.blit(display["image"], display["pos"])
            if display["text"]:
                self.draw_text_on_display(screen, display["text"], display["text_pos"])
    
    def draw_all_displays(self, screen):
        for display_name in self.displays:
            self.draw_display(screen, display_name)
    
    def draw_text_on_display(self, screen, text, pos):
        create_3d_text(screen, text, 12, pos[0], pos[1])
    
    def update_display_text(self, display_name, text):
        if display_name in self.displays:
            self.displays[display_name]["text"] = text
    
    def add_custom_display(self, name, image_type, pos, text_pos, text=""):
        if image_type in self.display_images:
            self.displays[name] = {
                "image": self.display_images[image_type],
                "pos": pos,
                "text_pos": text_pos,
                "text": text
            }

class ButtonManager:
    def __init__(self, console):
        self.console = console
        self.buttons = {}
        self.button_images = {}
        self.load_button_images()
        self.setup_button_positions()
    
    def load_button_images(self):
        self.button_images = {
            "info": self.console.reSize_Image(BUTTON_PATH + "but_info.png"),
            "mute": self.console.reSize_Image(BUTTON_PATH + "but_audio.png"),
            "pause": self.console.reSize_Image(BUTTON_PATH + "but_pause.png"),
            "reset": self.console.reSize_Image(BUTTON_PATH + "but_reset.png"),
            "play": self.console.reSize_Image(BUTTON_PATH + "but_play.png"),
            "exit": self.console.reSize_Image(BUTTON_PATH + "but_exit.png")
        }
    
    def setup_button_positions(self):
        self.button_positions = {
            "info": (10, 10),
            "mute": (110, 10),
            "pause": (self.console.screen_size - self.button_images["pause"].get_width() - 310, 10),
            "reset": (self.console.screen_size - self.button_images["reset"].get_width() - 210, 10),
            "play": (self.console.screen_size - self.button_images["play"].get_width() - 110, 10),
            "exit": (self.console.screen_size - self.button_images["exit"].get_width() - 10, 10),
        }
        
        for name, pos in self.button_positions.items():
            image = self.button_images[name]
            self.buttons[name] = {
                "image": image,
                "pos": pos,
                "rect": pygame.Rect(pos[0], pos[1], image.get_width(), image.get_height())
            }
    
    def draw_button(self, screen, button_name):
        if button_name in self.buttons:
            button = self.buttons[button_name]
            screen.blit(button["image"], button["pos"])
    
    def draw_all_buttons(self, screen):
        for button_name in self.buttons:
            self.draw_button(screen, button_name)
    
    def get_button_rect(self, button_name):
        if button_name in self.buttons:
            return self.buttons[button_name]["rect"]
        return None
    
    def update_button_icon(self, button_name, new_image_path, screen=None):
        """Cập nhật icon cho nút và tùy chọn vẽ lại ngay."""
        if button_name in self.buttons:
            new_image = self.console.reSize_Image(new_image_path)
            self.buttons[button_name]["image"] = new_image
            if screen:
                self.draw_button(screen, button_name)

def create_3d_text(screen, text, size, x, y):
    """Tạo hiệu ứng chữ 3D với viền"""
    
    font = pygame.font.Font(FONT, size)
    
    # Vẽ outline (viền)
    outline_offsets = [
        (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
        (-1, -2), (-1, 2),
        (0, -2), (0, 2),
        (1, -2), (1, 2),
        (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)
    ]
    
    for dx, dy in outline_offsets:
        outline_surface = font.render(text, True, BLUE_LIGHT)
        screen.blit(outline_surface, (x + dx, y + dy))
    
    # Vẽ chữ chính
    main_surface = font.render(text, True, WHITE)
    screen.blit(main_surface, (x, y))

class Menu_Display():
    def __init__(self, console):
        self.console = console

class ButtonMenu(ButtonManager):
    def load_button_images(self):
        self.button_images = {
            "info": self.console.reSize_Bigger_Image(BUTTON_PATH + "but_info.png"),
            "mute": self.console.reSize_Bigger_Image(BUTTON_PATH + "but_audio.png"),
            "play": self.console.reSize_Bigger_Image(BUTTON_PATH + "but_play.png"),
            "exit": self.console.reSize_Bigger_Image(BUTTON_PATH + "but_exit.png")
        }
    
    def setup_button_positions(self):
        self.button_positions = {
            "play": (self.console.screen_size // 5 - self.button_images["play"].get_width() // 2, self.console.screen_size // 3 * 2 - self.button_images["play"].get_height() // 2),
            "info": (self.console.screen_size // 5 * 2 - self.button_images["info"].get_width() // 2, self.console.screen_size // 3 * 2 - self.button_images["play"].get_height() // 2),
            "mute": (self.console.screen_size // 5 * 3 - self.button_images["mute"].get_width() // 2, self.console.screen_size // 3 * 2 - self.button_images["play"].get_height() // 2),
            "exit": (self.console.screen_size // 5 * 4 - self.button_images["exit"].get_width() // 2, self.console.screen_size // 3 * 2 - self.button_images["play"].get_height() // 2),
        }
        
        for name, pos in self.button_positions.items():
            image = self.button_images[name]
            self.buttons[name] = {
                "image": image,
                "pos": pos,
                "rect": pygame.Rect(pos[0], pos[1], image.get_width(), image.get_height())
            }

    def update_button_icon(self, button_name, new_image_path, screen=None):
        if button_name in self.buttons:
            new_image = self.console.reSize_Bigger_Image(new_image_path)
            self.buttons[button_name]["image"] = new_image
            if screen:
                self.draw_button(screen, button_name)

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
        self.button_menu.draw_all_buttons(surface)