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

        back_button_width = self.back_button.button_image.get_width()
        back_pos = (popup_center_x - back_button_width + 180, popup_center_y - back_button_width + 130)

        self.back_button.button_pos = back_pos
        self.back_button.update_img()
        
    def draw(self, screen):
        title_x = self.popup_pos[0] + self.popup_bg.get_width() // 2 - 110
        title_y = self.popup_pos[1] + 15
        create_3d_text(screen, "RUSH HOUR", 40, title_x, title_y)

        create_3d_text(screen, "GROUP 4", 25, title_x + 60, title_y + 50)
        create_3d_text(screen, "Tran Hoai Thien Nhan", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 120)
        create_3d_text(screen, "Tran Tri Nhan", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 160)
        create_3d_text(screen, "Nguyen An Nghiep", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 200)
        create_3d_text(screen, "Cao Tran Ba Dat", 16, self.popup_pos[0] + self.popup_bg.get_width() // 2 - 90, self.popup_pos[1] + 240)

        self.back_button.draw(screen)

    def check_button_click(self, mouse_pos):
        if not self.visible:
            return None
        
        for button_name, button_data in self.__dict__.items():
            if (button_name == 'back_button'
                and button_data.button["rect"].collidepoint(mouse_pos)):        
                return button_name
        return None
    