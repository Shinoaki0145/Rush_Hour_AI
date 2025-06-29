import pygame
from defs import *

class GamePopup:
    def __init__(self, console):
        self.console = console
        self.visible = False
        self.popup_type = None  # "algorithm" or "win"
        self.buttons = {}
        self.selected_option = None
        self.setup_popup()
        
        # Win popup specific data
        self.level = 1
        self.moves = 0
        self.algorithm = "IDS"
        
        # Load button images cho win popup
        self.win_button_images = {
            "reset_level": self.console.reSize_Image(BUTTON_PATH + "but_reset.png"),
            "next_level": self.console.reSize_Image(BUTTON_PATH + "but_play.png")
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
        self.selected_option = None
        self.setup_algorithm_buttons()
    
    def show_win_message(self, level, moves, algorithm="IDS"):
        self.popup_type = "win"
        self.visible = True
        self.level = level
        self.moves = moves
        self.algorithm = algorithm
        self.selected_option = None
        self.setup_win_buttons()
    
    def setup_algorithm_buttons(self):
        self.buttons = {}

        button_image = self.console.reSize_Image(BUTTON_PATH + "but_start.png")
        
        algorithms = ["BFS", "IDS", "A STAR", "UCS"]
        button_width = button_image.get_width()
        button_height = button_image.get_height()
        
        # Tính toán vị trí buttons (2x2 grid)
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2
        
        spacing_x = 20
        spacing_y = 20
        
        positions = [
            (popup_center_x - button_width - spacing_x//2, popup_center_y - button_height - spacing_y//2),  # BFS
            (popup_center_x + spacing_x//2, popup_center_y - button_height - spacing_y//2),  # IDS
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
        
        # Tính toán vị trí cho 2 buttons
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
    
    def hide(self):
        """Ẩn popup"""
        self.visible = False
        self.popup_type = None
    
    def draw(self, screen):
        """Vẽ popup và buttons"""
        if not self.visible:
            return
        
        # Vẽ popup background
        screen.blit(self.popup_bg, self.popup_pos)
        
        if self.popup_type == "algorithm":
            self.draw_algorithm_popup(screen)
        elif self.popup_type == "win":
            self.draw_win_popup(screen)
    
    def draw_algorithm_popup(self, screen):
        """Vẽ algorithm selection popup"""
        title_x = self.popup_pos[0] + self.popup_bg.get_width() // 2 - 120
        title_y = self.popup_pos[1] + 50
        create_3d_text(screen, "CHOOSE ALGORITHM", 24, title_x, title_y)
        
        for algorithm, button_data in self.buttons.items():
            screen.blit(button_data["image"], button_data["pos"])
            
            text_x = button_data["pos"][0] + button_data["image"].get_width() // 2 - len(algorithm) * 6
            text_y = button_data["pos"][1] + button_data["image"].get_height() // 2 - 10
            create_3d_text(screen, algorithm, 16, text_x, text_y)
    
    def draw_win_popup(self, screen):
        """Vẽ win message popup"""
        congrat_text = f"CONGRATULATIONS!"
        info_text = f"YOU WIN LEVEL {self.level} WITH {self.moves} MOVES"
        algorithm_text = f"BY USING ALGORITHM: {self.algorithm}"
        
        # Tính toán vị trí text
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        
        # Title
        title_x = popup_center_x - len(congrat_text) * 4 - 40
        title_y = self.popup_pos[1] + 50
        create_3d_text(screen, congrat_text, 20, title_x, title_y)
        
        # Info text
        info_x = popup_center_x - len(info_text) * 4 - 20
        info_y = self.popup_pos[1] + 100
        create_3d_text(screen, info_text, 16, info_x, info_y)
        
        # Algorithm text
        algorithm_x = popup_center_x - len(algorithm_text) * 4
        algorithm_y = self.popup_pos[1] + 130
        create_3d_text(screen, algorithm_text, 16, algorithm_x, algorithm_y)
        
        # Vẽ buttons - sử dụng button images có sẵn
        for button_name, button_data in self.buttons.items():
            # Vẽ button image
            screen.blit(button_data["image"], button_data["pos"])
    
    def check_button_click(self, mouse_pos):
        """Kiểm tra click vào buttons"""
        if not self.visible:
            return None
        
        for button_name, button_data in self.buttons.items():
            if button_data["rect"].collidepoint(mouse_pos):
                self.selected_option = button_name
                
                # KHÔNG tự động ẩn popup ở đây
                # Để game_manage.py xử lý việc ẩn popup
                
                return button_name
        return None

class DisplayManager:
    def __init__(self, console):
        self.console = console
        self.displays = {}
        self.load_display_images()
        self.setup_display_positions()
    
    def load_display_images(self):
        """Load các hình ảnh display"""
        self.display_images = {
            "algorithm": self.console.reSize_Image(DISPLAY_PATH + "algo_display.png"),
            "level": self.console.reSize_Image(DISPLAY_PATH + "level_display.png"),
            "moves": self.console.reSize_Image(DISPLAY_PATH + "moves_display.png"),
        }
    
    def setup_display_positions(self):
        """Setup vị trí cho các display"""
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
                "text": "LEVEL :  1"
            },
            "moves": {
                "image": self.display_images["moves"],
                "pos": (self.console.screen_size - 300, 175),
                "text_pos": (self.console.screen_size - 286, 179),
                "text": "MOVES :  0"
            }
        }
    
    def draw_display(self, screen, display_name):
        """Vẽ một display cụ thể"""
        if display_name in self.displays:
            display = self.displays[display_name]
            # Vẽ hình ảnh display
            screen.blit(display["image"], display["pos"])
            # Vẽ text lên display
            if display["text"]:
                self.draw_text_on_display(screen, display["text"], display["text_pos"])
    
    def draw_all_displays(self, screen):
        """Vẽ tất cả displays"""
        for display_name in self.displays:
            self.draw_display(screen, display_name)
    
    def draw_text_on_display(self, screen, text, pos):
        create_3d_text(screen, text, 12, pos[0], pos[1])
    
    def update_display_text(self, display_name, text):
        """Cập nhật text của display"""
        if display_name in self.displays:
            self.displays[display_name]["text"] = text
            print(f"DisplayManager: Updated {display_name} to: {text}")  # Debug line
    
    def add_custom_display(self, name, image_type, pos, text_pos, text=""):
        """Thêm display tùy chỉnh"""
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
        """Load tất cả button images"""
        self.button_images = {
            "info": self.console.reSize_Image(BUTTON_PATH + "but_info.png"),
            "mute": self.console.reSize_Image(BUTTON_PATH + "but_audio.png"),
            "pause": self.console.reSize_Image(BUTTON_PATH + "but_pause.png"),
            "reset": self.console.reSize_Image(BUTTON_PATH + "but_reset.png"),
            "play": self.console.reSize_Image(BUTTON_PATH + "but_play.png"),
            "exit": self.console.reSize_Image(BUTTON_PATH + "but_exit.png")
        }
    
    def setup_button_positions(self):
        """Setup vị trí của các button"""
        self.button_positions = {
            "info": (10, 10),
            "mute": (110, 10),
            "pause": (self.console.screen_size - self.button_images["pause"].get_width() - 310, 10),
            "reset": (self.console.screen_size - self.button_images["reset"].get_width() - 210, 10),
            "play": (self.console.screen_size - self.button_images["play"].get_width() - 110, 10),
            "exit": (self.console.screen_size - self.button_images["exit"].get_width() - 10, 10),
        }
        
        # Tạo button objects với thông tin đầy đủ
        for name, pos in self.button_positions.items():
            image = self.button_images[name]
            self.buttons[name] = {
                "image": image,
                "pos": pos,
                "rect": pygame.Rect(pos[0], pos[1], image.get_width(), image.get_height())
            }
    
    def draw_button(self, screen, button_name):
        """Vẽ một button cụ thể"""
        if button_name in self.buttons:
            button = self.buttons[button_name]
            screen.blit(button["image"], button["pos"])
    
    def draw_all_buttons(self, screen):
        """Vẽ tất cả buttons"""
        for button_name in self.buttons:
            self.draw_button(screen, button_name)
    
    def get_button_rect(self, button_name):
        """Lấy rect của button để check collision"""
        if button_name in self.buttons:
            return self.buttons[button_name]["rect"]
        return None

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