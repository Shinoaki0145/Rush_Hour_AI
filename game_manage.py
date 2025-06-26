import pygame
import ctypes
import console
import car
from map import *
import defs 
from manage_car import *

console = console.Console()
console.convertMatrix()

pygame.init()
screen = pygame.display.set_mode((console.screen_size, console.screen_size))
clock = pygame.time.Clock()
pygame.display.set_caption('Rush Hour') 
running = True  
board = Board(console.reSize_Image(MAP_PATH), SQUARE_SIZE_DEFAULT, 0, 0)

# Load button images
button_mute = console.reSize_Image("GUI/but_yes.png")
button_restart = console.reSize_Image("GUI/but_restart.png")
button_close = console.reSize_Image("GUI/but_exit.png")
button_next = console.reSize_Image("GUI/but_right.png")
button_prev = console.reSize_Image("GUI/but_left.png")

main_car = car.MainCar(1, 2, console.reSize_Image(MAIN_CAR_PATH))
print("PY")
car_1 = car.Car("car_1", 4, 0, console.reSize_Image(CAR_1), False, "down")

manage_car = ManageCar()   
manage_car.add_car(main_car)
#manage_car.add_car(car_1)

button_positions = {
    #"mute": (console.screen_size - button_mute.get_width() - 60, 10),
    "restart": (console.screen_size - button_restart.get_width() - 110, 10),
    "close": (console.screen_size - button_close.get_width() - 10, 10),
    #"next": (console.screen_size - button_next.get_width() - 10, 60),
    #"prev": (console.screen_size - button_prev.get_width() - 60, 60)
}

while running:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            exit()  
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                manage_car.move_car("main_car", "right")
            elif event.key == pygame.K_LEFT:
                manage_car.move_car("main_car", "left")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Check fullscreen button
            # if button_positions["fullscreen"][0] <= mouse_pos[0] <= button_positions["fullscreen"][0] + button_fullscreen.get_width() and \
            #    button_positions["fullscreen"][1] <= mouse_pos[1] <= button_positions["fullscreen"][1] + button_fullscreen.get_height():
            #     pygame.display.toggle_fullscreen()
            # Check mute button
            # elif button_positions["mute"][0] <= mouse_pos[0] <= button_positions["mute"][0] + button_mute.get_width() and \
            #      button_positions["mute"][1] <= mouse_pos[1] <= button_positions["mute"][1] + button_mute.get_height():
            #     pygame.mixer.music.set_volume(0 if pygame.mixer.music.get_volume() > 0 else 0.5)
            # Check restart button
            if button_positions["restart"][0] <= mouse_pos[0] <= button_positions["restart"][0] + button_restart.get_width() and \
                 button_positions["restart"][1] <= mouse_pos[1] <= button_positions["restart"][1] + button_restart.get_height():
                main_car.x, main_car.y = MATRIX[0][0][0], MATRIX[0][0][1]
            # Check close button
            elif button_positions["close"][0] <= mouse_pos[0] <= button_positions["close"][0] + button_close.get_width() and \
                 button_positions["close"][1] <= mouse_pos[1] <= button_positions["close"][1] + button_close.get_height():
                running = False
                exit()
            # Check next button
            # elif button_positions["next"][0] <= mouse_pos[0] <= button_positions["next"][0] + button_next.get_width() and \
            #      button_positions["next"][1] <= mouse_pos[1] <= button_positions["next"][1] + button_next.get_height():
            #     pass  # Add next level logic here
            # # Check prev button
            # elif button_positions["prev"][0] <= mouse_pos[0] <= button_positions["prev"][0] + button_prev.get_width() and \
            #      button_positions["prev"][1] <= mouse_pos[1] <= button_positions["prev"][1] + button_prev.get_height():
            #     pass  # Add previous level logic here

    screen.blit(board.image, (board.offset_x, board.offset_y))
    manage_car.update_car()

    manage_car.draw_all(screen)
    
    # Draw buttons
    #screen.blit(button_fullscreen, button_positions["fullscreen"])
    #screen.blit(button_mute, button_positions["mute"])
    screen.blit(button_restart, button_positions["restart"])
    screen.blit(button_close, button_positions["close"])
    #screen.blit(button_next, button_positions["next"])
    #screen.blit(button_prev, button_positions["prev"])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()



# import pygame

# # Khởi tạo Pygame
# pygame.init()

# # Cài đặt cửa sổ
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Hiệu ứng Neon Font")

# # Tải font (cần tải Bebas Neue trước, ví dụ từ Google Fonts)
# font = pygame.font.Font("font/arial.ttf", 72)  # Thay đường dẫn file font của bạn

# # Tạo văn bản
# text = font.render("PARKING BLOCK", True, (255, 255, 255))  # Màu trắng cho viền

# # Vòng lặp chính
# running = True
# clock = pygame.time.Clock()

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     screen.fill((0, 0, 0))  # Nền đen

#     # Tạo hiệu ứng neon (glow xanh dương)
#     for offset in range(15, 0, -2):  # Độ lan tỏa
#         glow = font.render("PARKING BLOCK", True, (0, 191, 255, offset * 10))  # Màu neon xanh
#         glow.set_alpha(offset * 10)  # Độ trong suốt
#         screen.blit(glow, (400 - text.get_width() // 2 + offset // 3, 300 - text.get_height() // 2 + offset // 3))

#     # Vẽ văn bản gốc lên trên với viền sáng
#     screen.blit(text, (400 - text.get_width() // 2, 300 - text.get_height() // 2))

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()