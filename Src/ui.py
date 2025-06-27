import pygame
from defs import *

class DisplayManager:
    def __init__(self, console):
        self.console = console
        self.displays = {}
        self.load_display_images()
        self.setup_display_positions()
    
    def load_display_images(self):
        """Load các hình ảnh display"""
        self.display_images = {
            "algorithm": self.console.reSize_Image("Asset/Display/algo_display.png"),
            "moves": self.console.reSize_Image("Asset/Display/moves_display.png"),  
            "level": self.console.reSize_Image("Asset/Display/level_display.png")
        }
    
    def setup_display_positions(self):
        """Setup vị trí cho các display"""
        self.displays = {
            "algorithm": {
                "image": self.display_images["algorithm"],
                "pos": (self.console.screen_size // 2 - 85, 175),
                "text_pos": (self.console.screen_size // 2 - 55, 179),
                "text": "ALGORITHM :   BFS"
            },
            "level": {
                "image": self.display_images["level"], 
                "pos": (205, 175),
                "text_pos": (222, 179),
                "text": "LEVEL :  12"
            },
            "moves": {
                "image": self.display_images["moves"],
                "pos": (self.console.screen_size - 300, 175),
                "text_pos": (self.console.screen_size - 286, 179),
                "text": "MOVES :  10"
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
            "info": self.console.reSize_Image("Asset/Button/but_info.png"),
            "mute": self.console.reSize_Image("Asset/Button/but_audio.png"),
            "pause": self.console.reSize_Image("Asset/Button/but_pause.png"),
            "reset": self.console.reSize_Image("Asset/Button/but_reset.png"),
            "play": self.console.reSize_Image("Asset/Button/but_play.png"),
            "exit": self.console.reSize_Image("Asset/Button/but_exit.png")
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

def create_3d_text(screen, text, size, x, y,):
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
    