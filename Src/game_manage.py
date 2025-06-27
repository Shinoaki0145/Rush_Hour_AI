import pygame
import console
import car
from board import *
from defs import *
from manage_car import *
from ui import *
from utils import GameUtils
from Algo import *

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
truck_0 = car.Car("truck_0", 4, 0, console.reSize_Image(CAR_PATH + "truck_0.png"), False, "down")
car_1 = car.Car("car_1", 4, 4, console.reSize_Image(CAR_PATH + "car_1.png"), True, "right")
car_2 = car.Car("car_2", 3, 3, console.reSize_Image(CAR_PATH + "car_2.png"), False, "down")

manage_car = ManageCar()   
manage_car.add_car(main_car)
manage_car.add_car(truck_0)
manage_car.add_car(car_1)
manage_car.add_car(car_2)

# Initialize UI and Utils
button_manager = ButtonManager(console)
display_manager = DisplayManager(console)
game_utils = GameUtils(console)

# Game objects dictionary for easy management
game_objects = {
    "main_car": main_car,
    "truck_0": truck_0,
    "car_1": car_1,
    "car_2": car_2,
    "manage_car": manage_car,
    "board": board
}

searched = False
path = []
current_step = 0
moves_count = 0
step_timer = 0
is_moving = False
waiting_for_next_step = False

while running:  
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            exit()  
        # elif event.type == pygame.KEYDOWN:
        #     game_objects = game_utils.handle_keyboard_input(event.key, game_objects)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            clicked_button = game_utils.check_button_click(mouse_pos, button_manager)
            if clicked_button:
                if clicked_button == "exit":
                    running = False
                    game_utils.handle_button_action(clicked_button, game_objects)
                elif clicked_button == "reset":
                    game_objects = game_utils.handle_button_action(clicked_button, game_objects)
                    # Reset algorithm variables
                    searched = False
                    path = []
                    current_step = 0
                    step_timer = 0
                    is_moving = False
                    waiting_for_next_step = False
                    moves_count = 0  # Reset moves count
                    start_time = pygame.time.get_ticks()  # Reset timer
                else:
                    game_objects = game_utils.handle_button_action(clicked_button, game_objects)

    # Run search
    if not searched:
        cars = []
        for car in game_objects["manage_car"].cars.values():
            cars.append(SimpleCar(car.name, car.length_grid, (car.y, car.x), not car.is_horizontal))
        start = State(cars)
        path = ids(start)
        #i = 0
        current_step = 0
        step_timer = current_time
        searched = True
        print(f"Found path with {len(path)} steps")

    display_manager.update_display_text("ALGORITHM", "ALGORITHM: BFS")
    display_manager.update_display_text("LEVEL", "LEVEL: 1")

    # Draw game elements
    screen.blit(game_objects["board"].image, (game_objects["board"].offset_x, game_objects["board"].offset_y))
    
    # if not game_objects["manage_car"].update_car():
    #     if i < len(path):
    #         for car in path[i].cars:
    #             game_objects["manage_car"].cars[car.name].y, game_objects["manage_car"].cars[car.name].x = car.coord
    #     i += 1
    
        # Algorithm execution with step timing
    if searched and path:
        # Kiểm tra xem có xe nào đang di chuyển không
        cars_moving = game_objects["manage_car"].update_car()
        
        if not cars_moving:  # Không có xe nào đang di chuyển
            if waiting_for_next_step:
                # Đang chờ để thực hiện step tiếp theo
                if current_time - step_timer >= STEP_DELAY:
                    waiting_for_next_step = False
                    current_step += 1
            else:
                # Thực hiện step tiếp theo nếu còn
                if current_step < len(path):
                    # Cập nhật vị trí xe theo step hiện tại
                    for car in path[current_step].cars:
                        if car.name in game_objects["manage_car"].cars:
                            game_objects["manage_car"].cars[car.name].y, game_objects["manage_car"].cars[car.name].x = car.coord
                    
                    moves_count += 1  # Tăng số bước di chuyển
                    # Cập nhật hiển thị số bước di chuyển
                    display_manager.update_display_text("MOVES", f"MOVES: {moves_count}")
                    
                    print(f"Executing step {current_step + 1}/{len(path)}")
                    
                    # Bắt đầu đếm thời gian chờ cho step tiếp theo
                    step_timer = current_time
                    waiting_for_next_step = True
                else:
                    print(f"Algorithm execution completed! Total moves: {moves_count}")
    else:
        # Fallback cho trường hợp không có path hoặc chưa search
        if not game_objects["manage_car"].update_car():
            if current_step < len(path):
                for car in path[current_step].cars:
                    game_objects["manage_car"].cars[car.name].y, game_objects["manage_car"].cars[car.name].x = car.coord
            current_step += 1

    game_objects["manage_car"].draw_all(screen)
    
    # Draw UI elements
    button_manager.draw_all_buttons(screen)
    display_manager.draw_all_displays(screen)
    create_3d_text(screen, "RUSH HOUR", 80, 180, console.screen_size - 96)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()