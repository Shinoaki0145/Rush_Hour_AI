import pygame
from defs import *

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
            "exit": self.console.reSize_Image("Asset/Button/but_exit.png")
        }
    
    def setup_button_positions(self):
        """Setup vị trí của các button"""
        self.button_positions = {
            "info": (10, 10),
            "mute": (110, 10),
            "pause": (self.console.screen_size - self.button_images["pause"].get_width() - 210, 10),
            "reset": (self.console.screen_size - self.button_images["reset"].get_width() - 110, 10),
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

def create_3d_text(screen, text, x, y,):
    """Tạo hiệu ứng chữ 3D với viền"""
    
    font = pygame.font.Font(FONT, 80)  # Sử dụng font đã định nghĩa trong defs.py
    
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
    
    