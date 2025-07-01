import pygame
from defs import *
from Cars import *

class GamePopup:
    def __init__(self, console):
        self.console = console
        self.visible = False
        self.popup_type = None  # "algorithm", "win", "lose", or "final_win"
        self.buttons = {}
        self.setup_popup()
        
        # Win popup specific data
        self.level = 0
        self.moves = 0
        self.cost = 0
        self.algorithm = ""
        
        # Load button images cho win popup
        self.win_button_images = {
            "reset_level": self.console.reSize_Image(BUTTON_PATH + "but_reset.png"),
            "next_level": self.console.reSize_Image(BUTTON_PATH + "but_play.png")
        }
        
        # Load button images cho lose popup
        self.lose_button_images = {
            "reset_level": self.console.reSize_Image(BUTTON_PATH + "but_reset.png"),
            "exit_level": self.console.reSize_Image(BUTTON_PATH + "but_exit.png")
        }
        
        self.final_win_1_button_images = {
            "exit_level": self.console.reSize_Image(BUTTON_PATH + "but_exit.png"),
            "next_popup": self.console.reSize_Image(BUTTON_PATH + "but_play.png")  # Dùng play button cho "next"
        }
        self.final_win_2_button_images = {
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
        
    def show_final_win_1_message(self, level, moves, cost, algorithm="DFS"):
        """Hiển thị final win popup đầu tiên (giống win popup nhưng có exit và next)"""
        self.popup_type = "final_win_1"
        self.visible = True
        self.level = level
        self.moves = moves
        self.cost = cost
        self.algorithm = algorithm
        self.setup_final_win_1_buttons()
    
    def show_final_win_2_message(self):
        """Hiển thị final win popup thứ hai (level selection)"""
        self.popup_type = "final_win_2"
        self.visible = True
        self.setup_final_win_2_buttons()

    def show_info_in_game(self):
        """Hiển thị thông tin các nút trên màn hình"""
        self.popup_type = "info_buttons"
        self.visible = True
        self.selected_option = None
        self.setup_info_in_game()

    def show_info_menu(self):
        """Hiển thị thông tin các thông tin thành viên trên màn hình"""
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
        
        # Tính toán vị trí buttons (2x2 grid)
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

    def setup_lose_buttons(self):
        self.buttons = {}

        reset_button_image = self.lose_button_images["reset_level"]
        exit_button_image = self.lose_button_images["exit_level"]

        # Tính toán vị trí cho 2 buttons
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
        
    def setup_final_win_1_buttons(self):
        """Setup buttons cho final_win_1 popup"""
        self.buttons = {}

        exit_button_image = self.final_win_1_button_images["exit_level"]
        next_button_image = self.final_win_1_button_images["next_popup"]
        
        # Tính toán vị trí cho 2 buttons (giống như win popup)
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
        
    def setup_final_win_2_buttons(self):
        """Setup buttons cho final_win_2 popup (level selection - 3 dòng × 4 cột)"""
        self.buttons = {}

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
    def setup_info_in_game(self):
        self.buttons = {}

        play_button_image = self.info_in_game["play_button"]
        pause_button_image = self.info_in_game["pause_button"]
        exit_button_image = self.info_in_game["exit_button"]
        back_button_image = self.info_in_game["back_button"]

        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2

        button_image = self.console.reSize_Image(BUTTON_PATH + "but_start.png")

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
        elif self.popup_type == "lose":
            self.draw_lose_popup(screen)
        elif self.popup_type == "final_win_1":
            self.draw_final_win_1_popup(screen)
        elif self.popup_type == "final_win_2":
            self.draw_final_win_2_popup(screen)
        elif self.popup_type == "info_buttons":
            self.draw_info_in_game(screen)
        elif self.popup_type == "info_menu":
            self.draw_info_menu(screen)
    
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
        info_text_1 = f"YOU WIN LEVEL {self.level}"
        info_text_2 = f"WITH {self.moves} MOVES AND COST {self.cost} UNITS"
        algorithm_text = f"BY USING ALGORITHM: {self.algorithm}"
        
        # Tính toán vị trí text
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        
        # Title
        title_x = popup_center_x - len(congrat_text) * 4 - 40
        title_y = self.popup_pos[1] + 30
        create_3d_text(screen, congrat_text, 20, title_x, title_y)
        
        # Info text
        info_x = popup_center_x - len(info_text_1) * 4 - 20
        info_y = self.popup_pos[1] + 80
        create_3d_text(screen, info_text_1, 16, info_x, info_y)
        
        info_x_2 = popup_center_x - len(info_text_2) * 4 - 20
        info_y_2 = self.popup_pos[1] + 100
        create_3d_text(screen, info_text_2, 16, info_x_2, info_y_2)

        # Algorithm text
        algorithm_x = popup_center_x - len(algorithm_text) * 4
        algorithm_y = self.popup_pos[1] + 120
        create_3d_text(screen, algorithm_text, 16, algorithm_x, algorithm_y)
        
        # Vẽ buttons - sử dụng button images có sẵn
        for button_name, button_data in self.buttons.items():
            # Vẽ button image
            screen.blit(button_data["image"], button_data["pos"])
    
    def draw_lose_popup(self, screen):
        """Vẽ lose message popup"""
        congrat_text = f"YOU LOST!"
        info_text = f"YOU FAILED LEVEL {self.level}"
        algorithm_text = f"BY USING ALGORITHM: {self.algorithm}"
        
        # Tính toán vị trí text
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        
        # Title
        title_x = popup_center_x - len(congrat_text) * 4 - 20
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
    
    def draw_final_win_1_popup(self, screen):
        """Vẽ final win 1 popup (giống win popup)"""
        congrat_text = f"CONGRATULATIONS!"
        info_text_1 = f"YOU WIN LEVEL {self.level}"
        info_text_2 = f"WITH {self.moves} MOVES AND COST {self.cost} UNITS"
        algorithm_text = f"BY USING ALGORITHM: {self.algorithm}"
        
        # Tính toán vị trí text
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        
        # Title
        title_x = popup_center_x - len(congrat_text) * 4 - 40
        title_y = self.popup_pos[1] + 30
        create_3d_text(screen, congrat_text, 20, title_x, title_y)
        
        # Info text
        info_x = popup_center_x - len(info_text_1) * 4 - 20
        info_y = self.popup_pos[1] + 80
        create_3d_text(screen, info_text_1, 16, info_x, info_y)
        
        info_x_2 = popup_center_x - len(info_text_2) * 4 - 20
        info_y_2 = self.popup_pos[1] + 100
        create_3d_text(screen, info_text_2, 16, info_x_2, info_y_2)

        # Algorithm text
        algorithm_x = popup_center_x - len(algorithm_text) * 4
        algorithm_y = self.popup_pos[1] + 120
        create_3d_text(screen, algorithm_text, 16, algorithm_x, algorithm_y)
        
        # Vẽ buttons
        for button_name, button_data in self.buttons.items():
            screen.blit(button_data["image"], button_data["pos"])
    
    def draw_final_win_2_popup(self, screen):
        win_text = "Select a level to start playing"
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        win_text_x = popup_center_x - len(win_text) * 4 - 17 #Chu 
        win_text_y = self.popup_pos[1] + 20  # Di chuyển lên cao hơn (giảm từ 40 xuống 20)
        create_3d_text(screen, win_text, 20, win_text_x, win_text_y)
        
        # Vẽ level buttons (3 dòng × 4 cột), điều chỉnh vị trí y của nút
        for button_name, button_data in self.buttons.items():
            # Tăng vị trí y của nút để tránh đè lên chữ (ví dụ: +20)
            adjusted_pos = (button_data["pos"][0], button_data["pos"][1] + 20)
            screen.blit(button_data["image"], adjusted_pos)
            level_text = button_data["text"]
            text_x = adjusted_pos[0] + button_data["image"].get_width() // 2 - len(level_text) * 4
            text_y = adjusted_pos[1] + button_data["image"].get_height() // 2 - 15
            create_3d_text(screen, level_text, 20, text_x, text_y)
    def draw_info_in_game(self, screen):
        """Vẽ info popup"""
        title_x = self.popup_pos[0] + self.popup_bg.get_width() // 2 - 135
        title_y = self.popup_pos[1] + 15
        create_3d_text(screen, "INFO BUTTON IN GAME", 24, title_x, title_y)

        create_3d_text(screen, "Press play to choose Algorithm", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 80)
        create_3d_text(screen, "Press pause to pause game and", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 140)
        create_3d_text(screen, "press again to continue", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 160)
        create_3d_text(screen, "Press exit to out game", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 220)

        for button_name, button_data in self.buttons.items():
            screen.blit(button_data["image"], button_data["pos"])
    
    def draw_info_menu(self, screen):
        title_x = self.popup_pos[0] + self.popup_bg.get_width() // 2 - 110
        title_y = self.popup_pos[1] + 15
        create_3d_text(screen, "RUSH HOUR", 40, title_x, title_y)

        create_3d_text(screen, "GROUP 4", 25, title_x + 60, title_y + 50)
        create_3d_text(screen, "Tran Hoai Thien Nhan", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 120)
        create_3d_text(screen, "Tran Tri Nhan", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 160)
        create_3d_text(screen, "Nguyen An Nghiep", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 200)
        create_3d_text(screen, "Cao Tran Ba Dat", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 240)

        for button_name, button_data in self.buttons.items():
            screen.blit(button_data["image"], button_data["pos"])

    def check_button_click(self, mouse_pos):
        """Kiểm tra click vào buttons"""
        if not self.visible:
            return None
        
        for button_name, button_data in self.buttons.items():
            if button_data["rect"].collidepoint(mouse_pos):
                # KHÔNG tự động ẩn popup ở đây
                # Để game_manage.py xử lý việc ẩn popup
                
                return button_name
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
