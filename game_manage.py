# import pygame
# import console
# import car
# from map import *
# from defs import *
# from manage_car import *
# from ui import *

# pygame.init()
# console = console.Console()
# console.convertMatrix()

# screen = pygame.display.set_mode((console.screen_size, console.screen_size))
# clock = pygame.time.Clock()
# pygame.display.set_caption('Rush Hour') 
# running = True  
# board = Board(console.reSize_Image(MAP_PATH), SQUARE_SIZE_DEFAULT, 0, 0)


# main_car = car.MainCar(0, 2, console.reSize_Image(MAIN_CAR_PATH))
# car_1 = car.Car("car_1", 4, 0, console.reSize_Image(CAR_1), False, "down")

# manage_car = ManageCar()   
# manage_car.add_car(main_car)
# manage_car.add_car(car_1)

# # Load button images
# button_info = console.reSize_Image("Asset/Button/but_info.png")
# button_mute = console.reSize_Image("Asset/Button/but_audio.png")
# button_stop = console.reSize_Image("Asset/Button/but_reset.png")
# button_reset = console.reSize_Image("Asset/Button/but_reset.png")
# button_exit = console.reSize_Image("Asset/Button/but_exit.png")

# button_positions = {
#     "info": (10, 10),
#     "mute": (110, 10),
#     "stop": (console.screen_size - button_stop.get_width() - 210, 10),
#     "reset": (console.screen_size - button_reset.get_width() - 110, 10),
#     "exit": (console.screen_size - button_exit.get_width() - 10, 10),
# }

# while running:  
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
#             running = False
#             exit()  
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RIGHT:
#                 manage_car.move_car("main_car", "right")
#             elif event.key == pygame.K_LEFT:
#                 manage_car.move_car("main_car", "left")
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             mouse_pos = event.pos
#             if (button_positions["reset"][0] <= mouse_pos[0] <= button_positions["reset"][0] + button_reset.get_width() and
#                  button_positions["reset"][1] <= mouse_pos[1] <= button_positions["reset"][1] + button_reset.get_height()):
#                 # Reset the game state
#                 main_car = car.MainCar(0, 2, console.reSize_Image(MAIN_CAR_PATH))
#                 car_1 = car.Car("car_1", 4, 0, console.reSize_Image(CAR_1), False, "down")

#                 manage_car = ManageCar()   
#                 manage_car.add_car(main_car)
#                 manage_car.add_car(car_1)
                
#             # Check close button
#             elif (button_positions["exit"][0] <= mouse_pos[0] <= button_positions["exit"][0] + button_exit.get_width() and
#                  button_positions["exit"][1] <= mouse_pos[1] <= button_positions["exit"][1] + button_exit.get_height()):
#                 running = False
#                 exit()
                
#             # Check stop button
#             elif (button_positions["stop"][0] <= mouse_pos[0] <= button_positions["stop"][0] + button_stop.get_width() and
#                  button_positions["stop"][1] <= mouse_pos[1] <= button_positions["stop"][1] + button_stop.get_height()):
#                 # Stop the game logic
#                 manage_car.stop_all_cars()
                
#             # Check mute button
#             elif (button_positions["mute"][0] <= mouse_pos[0] <= button_positions["mute"][0] + button_mute.get_width() and
#                  button_positions["mute"][1] <= mouse_pos[1] <= button_positions["mute"][1] + button_mute.get_height()):
#                 # Mute or unmute the game sounds
#                 console.toggle_audio()
                
#             # Check info button
#             elif (button_positions["info"][0] <= mouse_pos[0] <= button_positions["info"][0] + button_info.get_width() and
#                  button_positions["info"][1] <= mouse_pos[1] <= button_positions["info"][1] + button_info.get_height()):
#                 # Show game information
#                 console.show_info()

#     screen.blit(board.image, (board.offset_x, board.offset_y))
#     manage_car.update_car()

#     manage_car.draw_all(screen)
    
#     # Draw buttons
#     screen.blit(button_mute, button_positions["mute"])
#     screen.blit(button_reset, button_positions["reset"])
#     screen.blit(button_exit, button_positions["exit"])
#     screen.blit(button_stop, button_positions["stop"])
#     screen.blit(button_info, button_positions["info"])
    
#     # Draw 3D text
#     create_3d_text(screen, "RUSH HOUR", 180, console.screen_size - 100)

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()


import pygame
import console
import car
from map import *
from defs import *
from manage_car import *
from ui import ButtonManager, create_3d_text
from utils import GameUtils

pygame.init()
console = console.Console()
console.convertMatrix()

screen = pygame.display.set_mode((console.screen_size, console.screen_size))
clock = pygame.time.Clock()
pygame.display.set_caption('Rush Hour') 
running = True  
board = Board(console.reSize_Image(MAP_PATH), SQUARE_SIZE_DEFAULT, 0, 0)

# Initialize game objects
main_car = car.MainCar(0, 2, console.reSize_Image(MAIN_CAR_PATH))
car_1 = car.Car("car_1", 4, 0, console.reSize_Image(CAR_1), False, "down")

manage_car = ManageCar()   
manage_car.add_car(main_car)
manage_car.add_car(car_1)

# Initialize UI and Utils
button_manager = ButtonManager(console)
game_utils = GameUtils(console)

# Game objects dictionary for easy management
game_objects = {
    "main_car": main_car,
    "car_1": car_1,
    "manage_car": manage_car,
    "board": board
}

while running:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            exit()  
        elif event.type == pygame.KEYDOWN:
            game_objects = game_utils.handle_keyboard_input(event.key, game_objects)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            clicked_button = game_utils.check_button_click(mouse_pos, button_manager)
            if clicked_button:
                if clicked_button == "exit":
                    running = False
                    game_utils.handle_button_action(clicked_button, game_objects)
                else:
                    game_objects = game_utils.handle_button_action(clicked_button, game_objects)

    # Draw game elements
    screen.blit(game_objects["board"].image, (game_objects["board"].offset_x, game_objects["board"].offset_y))
    game_objects["manage_car"].update_car()
    game_objects["manage_car"].draw_all(screen)
    
    # Draw UI elements
    button_manager.draw_all_buttons(screen)
    create_3d_text(screen, "RUSH HOUR", 180, console.screen_size - 100)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()