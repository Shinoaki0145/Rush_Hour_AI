from .popup_base import *

class PopupFinalWin2(PopupBase):
    def __init__(self, console):
        super().__init__(console)

        self.buttons = {}
        self.final_win_2_button_images = {
            "level_button": self.console.reSize_Image(BUTTON_PATH + "level_unlock.png"),
        }

    def show(self):
        """Hiển thị final win popup thứ hai (level selection)"""
        self.setup()

    def setup(self):
        """Setup buttons cho final_win_2 popup (level selection - 3 dòng × 4 cột)"""
        level_button_image = self.final_win_2_button_images["level_button"]
        button_width = level_button_image.get_width()
        button_height = level_button_image.get_height()

        # Calculate positions for 12 level buttons (3 rows × 4 columns)
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2
        spacing_x = 15  # Giảm khoảng cách ngang để vừa 4 cột
        spacing_y = 15  # Giảm khoảng cách dọc để vừa 3 dòng

        # Tính toán vị trí bắt đầu để căn giữa grid 3×4
        total_width = 4 * button_width + 3 * spacing_x
        total_height = 3 * button_height + 2 * spacing_y
        
        start_x = popup_center_x - total_width // 2
        start_y = popup_center_y - total_height // 2

        for i in range(12):
            row = i // 4  # Chia cho 4 để có 3 dòng
            col = i % 4   # Chia lấy dư cho 4 để có 4 cột
            
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

    def draw(self, screen):
        win_text = "Select a level to start playing"
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        win_text_x = popup_center_x - len(win_text) * 4 - 17 #Chu 
        win_text_y = self.popup_pos[1] + 20  # Di chuyển lên cao hơn (giảm từ 40 xuống 20)
        create_3d_text(screen, win_text, 20, win_text_x, win_text_y)
        
        # Vẽ level buttons (3 dòng × 4 cột), điều chỉnh vị trí y của nút
        for _, button_data in self.buttons.items():
            # Tăng vị trí y của nút để tránh đè lên chữ (ví dụ: +20)
            adjusted_pos = (button_data["pos"][0], button_data["pos"][1] + 20)
            screen.blit(button_data["image"], adjusted_pos)
            level_text = button_data["text"]
            text_x = adjusted_pos[0] + button_data["image"].get_width() // 2 - len(level_text) * 4
            text_y = adjusted_pos[1] + button_data["image"].get_height() // 2 - 15
            create_3d_text(screen, level_text, 20, text_x, text_y)

    def check_button_click(self, mouse_pos):
        for button_name, button_data in self.buttons.items():
            if button_data["rect"].collidepoint(mouse_pos):
                return button_name
        return None