from .popup_base import  *
import UI.Button.button_back as bb

class PopupInfoMenu(PopupBase):
    def __init__(self, console):
        super().__init__(console)
        self.back_button = bb.ButtonBack(console)

    def show(self):
        self.visible = True
        self.setup()

    def setup(self):
        popup_center_x = self.popup_pos[0] + self.popup_bg.get_width() // 2
        popup_center_y = self.popup_pos[1] + self.popup_bg.get_height() // 2

        x, y = self.console.convertCoordinate(215, 160)
        back_button_width = self.back_button.button_image.get_width()
        back_pos = (popup_center_x - back_button_width + x, popup_center_y - back_button_width + y)

        self.back_button.button_pos = back_pos
        self.back_button.update_img()
        
    def draw(self, screen):
        x, y = self.console.convertCoordinate(120, 20)
        create_3d_text(screen, "RUSH HOUR", 60, self.popup_pos[0] + self.popup_bg.get_width() // 2 - x, self.popup_pos[1] + y, self.console)

        x, y = self.console.convertCoordinate(70, 80)
        create_3d_text(screen, "GROUP 4", 40, self.popup_pos[0] + self.popup_bg.get_width() // 2 - x, self.popup_pos[1] + y, self.console)
        
        x, y = self.console.convertCoordinate(100, 140)
        create_3d_text(screen, "Tran Hoai Thien Nhan", 30, self.popup_pos[0] + self.popup_bg.get_width() // 2 - x, self.popup_pos[1] + y, self.console)
        x, y = self.console.convertCoordinate(100, 180)
        create_3d_text(screen, "Tran Tri Nhan", 30, self.popup_pos[0] + self.popup_bg.get_width() // 2 - x, self.popup_pos[1] + y, self.console)
        x, y = self.console.convertCoordinate(100, 220)
        create_3d_text(screen, "Nguyen An Nghiep", 30, self.popup_pos[0] + self.popup_bg.get_width() // 2 - x, self.popup_pos[1] + y, self.console)
        x, y = self.console.convertCoordinate(100, 260)
        create_3d_text(screen, "Cao Tran Ba Dat", 30, self.popup_pos[0] + self.popup_bg.get_width() // 2 - x, self.popup_pos[1] + y, self.console)

        self.back_button.draw(screen)

    def check_button_click(self, mouse_pos):
        if not self.visible:
            return None
        
        for button_name, button_data in self.__dict__.items():
            if (button_name == 'back_button'
                and button_data.button["rect"].collidepoint(mouse_pos)):        
                return button_name
        return None
    